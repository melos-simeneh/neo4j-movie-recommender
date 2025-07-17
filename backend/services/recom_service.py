from utils.neo4j_db import query_neo4j
from utils import lib

async def get_all_users(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    query = """
    MATCH (u:User)
    RETURN u.userId AS userId, u.username AS username, u.full_name AS full_name
    ORDER BY u.userId ASC
    SKIP $skip
    LIMIT $limit
    """
    return await query_neo4j(query, {"skip": skip, "limit": page_size})


async def get_all_movies(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size

    # Query to fetch paginated movie data
    movie_query = """
    MATCH (m:Movie)
    RETURN 
        m.movieId AS movieId,
        m.title AS title,
        m.genres AS genres,
        m.imdbId AS imdbId,
        m.tmdbId AS tmdbId
    ORDER BY m.movieId ASC
    SKIP $skip
    LIMIT $limit
    """

    # Query to count total movies
    count_query = "MATCH (m:Movie) RETURN count(m) AS total"

    # Run both queries
    movies = await query_neo4j(movie_query, {"skip": skip, "limit": page_size})
    total_result = await query_neo4j(count_query)

    total = total_result[0]["total"] if total_result else 0

    return {
        "movies": movies,
        "total": total,
        "page": page,
        "page_size": page_size
    }


async def collaborative_recommendation(user_id: int):
    query = """
MATCH (u1:User {userId: $user_id})-[:RATED]->(m1:Movie)
WITH u1, collect(m1) AS u1Movies

MATCH (u2:User)-[:RATED]->(m2:Movie)
WHERE u1 <> u2
WITH u1, u1Movies, u2, collect(m2) AS u2Movies

WITH u1, u2, u1Movies,
     apoc.coll.intersection(u1Movies, u2Movies) AS sharedMovies,
     apoc.coll.union(u1Movies, u2Movies) AS allMovies
WITH u1, u2, u1Movies,
     size(sharedMovies) AS sharedRatedMoviesCount,
     size(allMovies) AS allRatedMoviesCount,
     (size(sharedMovies)*1.0)/size(allMovies) AS jaccard
WHERE jaccard > 0.1
ORDER BY sharedRatedMoviesCount DESC
LIMIT 25

// Capture similarity info
WITH u1, u1Movies, u2, sharedRatedMoviesCount, jaccard

MATCH (u2)-[r2:RATED]->(rec:Movie)
WHERE NOT EXISTS {
    MATCH (u1)-[:RATED]->(rec)
}

// carry metadata early
WITH rec, r2.rating AS rating, u2.userId AS userId, u2.full_name AS full_name,
     sharedRatedMoviesCount, jaccard

WITH rec.movieId AS movieId,
     rec.title AS title,
     {
         userId: userId,
         full_name: full_name,
         rating: rating,
         sharedRatedMoviesCount: sharedRatedMoviesCount,
         jaccard: jaccard
     } AS recommenderInfo

WITH movieId, title, collect(recommenderInfo) AS recommenders
WITH movieId, title, recommenders,
     reduce(score = 0.0, r IN recommenders | score + r.sharedRatedMoviesCount * r.rating) AS score,
     size(recommenders) AS totalSimilarUsersWhoRated

UNWIND recommenders AS r
WITH movieId, title, score, totalSimilarUsersWhoRated, r
ORDER BY r.sharedRatedMoviesCount DESC
WITH movieId, title, score, totalSimilarUsersWhoRated, collect(r)[0..5] AS top5Recommenders

RETURN movieId, title, score, totalSimilarUsersWhoRated, top5Recommenders
ORDER BY score DESC
LIMIT 10

    """
    return await query_neo4j(query, {"user_id": user_id})




async def content_based_recommendation(user_id: int):
    query = """
    MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
    WHERE r.rating >= 4.0
    WITH u, collect(m) AS likedMovies

    UNWIND likedMovies AS lm
    MATCH (lm)-[:HAS_GENRE]->(g:Genre)
    WITH u, collect(DISTINCT g.name) AS likedGenreNames, likedMovies

    UNWIND likedMovies AS lm
    MATCH (lm)-[:HAS_TAG]->(t:Tag)
    WITH u, likedGenreNames, collect(DISTINCT t.name) AS likedTagNames

    MATCH (rec:Movie)
    WHERE NOT EXISTS {
      MATCH (u)-[:RATED]->(rec)
    }

    OPTIONAL MATCH (rec)-[:HAS_GENRE]->(g2:Genre)
    WITH u, rec, likedGenreNames, likedTagNames, collect(DISTINCT g2.name) AS recGenres

    OPTIONAL MATCH (rec)-[:HAS_TAG]->(t2:Tag)
    WITH u, rec, likedGenreNames, likedTagNames, recGenres, collect(DISTINCT t2.name) AS recTags

    WITH rec,
         [g IN recGenres WHERE g IN likedGenreNames] AS sharedGenres,
         [t IN recTags WHERE t IN likedTagNames] AS sharedTags

    WITH rec.movieId AS movieId,
         rec.title AS title,
         sharedGenres,
         sharedTags,
         size(sharedGenres) AS genreScore,
         size(sharedTags) AS tagScore,
         (size(sharedGenres) * 1.5 + size(sharedTags)) AS score

    WHERE score > 0
    RETURN movieId, title, score, genreScore, tagScore, sharedGenres, sharedTags
    ORDER BY score DESC
    LIMIT 10
    """
    return await query_neo4j(query, {"user_id": user_id})

async def context_based_recommendation(user_id: int):
    query = """
MATCH (u:User {userId: $user_id})-[:RATED]->(m1:Movie)
WITH u, collect(m1) AS userMovies

MATCH (other:User)-[r:RATED]->(m:Movie)
WHERE other <> u

WITH u, other, r, m, userMovies,
     datetime() AS now, 
     datetime({epochMillis: r.timestamp * 1000}) AS ratingDate

WITH u, other, r, m, userMovies,
     duration.inDays(ratingDate, now).days AS daysSinceRating

WITH u, other, r, m,
     exp(-0.01 * daysSinceRating) AS recencyWeight

WITH m, r, exp(-0.01 * duration.inDays(datetime({epochMillis: r.timestamp * 1000}), datetime()).days) * r.rating AS weighted
WITH m, sum(weighted) AS weightedScore

// Gather all ratings for the movie to compute avg and count
MATCH (m)<-[allRatings:RATED]-()
WITH m, weightedScore,
     avg(allRatings.rating) AS averageRating,
     count(allRatings) AS numRatings

// Collect recent raters sorted by timestamp desc (most recent first)
OPTIONAL MATCH (recentRater:User)-[recentRating:RATED]->(m)
WITH m, weightedScore, averageRating, numRatings, recentRater, recentRating
ORDER BY recentRating.timestamp DESC
WITH m, weightedScore, averageRating, numRatings,
     collect({
       userId: recentRater.userId,
       name: recentRater.full_name,
       rating: recentRating.rating,
       ratedAt: recentRating.timestamp
     })[0..2] AS recentRaters

// Set latestRatingDate based on the most recent rater's timestamp, fallback to null
WITH m, weightedScore, averageRating, numRatings, recentRaters,
     CASE 
       WHEN size(recentRaters) > 0 THEN datetime({epochMillis: recentRaters[0].ratedAt * 1000})
       ELSE null
     END AS latestRatingDate

RETURN m.movieId AS movieId,
       m.title AS title,
       weightedScore,
       averageRating,
       numRatings,
       latestRatingDate,
       recentRaters
ORDER BY weightedScore DESC
LIMIT 10

    """
    records= await query_neo4j(query, {"user_id": user_id})
    return [
    {
        **record,
        "latestRatingDate": lib.format_timestamp(record.get("latestRatingDate")),
        "recentRaters": [
            {
                **dict(r),
                "ratedAt": lib.format_timestamp(r.get("ratedAt"))
            }
            for r in record.get("recentRaters", [])
        ],
    }
    for record in map(dict, records)
]
    
    
    
async def hybrid_recommendation(user_id: int):
    query = """
       MATCH (targetUser:User {userId: $user_id})-[:RATED]->(targetUserMovie:Movie)
WITH targetUser, collect(targetUserMovie) AS targetUserMovies

// Find similar users by Jaccard index on rated movies
MATCH (otherUser:User)-[:RATED]->(otherUserMovie:Movie)
WHERE targetUser <> otherUser
WITH targetUser, targetUserMovies, otherUser, collect(otherUserMovie) AS otherUserMovies

WITH targetUser, otherUser, targetUserMovies,
    apoc.coll.intersection(targetUserMovies, otherUserMovies) AS sharedMovies,
    apoc.coll.union(targetUserMovies, otherUserMovies) AS allMovies
WITH targetUser, otherUser, targetUserMovies, size(sharedMovies)*1.0/size(allMovies) AS jaccardSimilarity
WHERE jaccardSimilarity > 0.1
ORDER BY jaccardSimilarity DESC
LIMIT 25

// Candidate movies rated by similar users but not yet rated by target user
MATCH (otherUser)-[ratingRel:RATED]->(candidateMovie:Movie)
WHERE NOT EXISTS {
    MATCH (targetUser)-[:RATED]->(candidateMovie)
}

// Shared genres between user’s rated movies and candidate movie
OPTIONAL MATCH (targetUser)-[:RATED]->(:Movie)-[:HAS_GENRE]->(genre:Genre)<-[:HAS_GENRE]-(candidateMovie)

// Shared tags between user’s tagged movies and candidate movie
OPTIONAL MATCH (targetUser)-[:TAGGED]->(:Movie)-[:HAS_TAG]->(tag:Tag)<-[:HAS_TAG]-(candidateMovie)

WITH candidateMovie, jaccardSimilarity, otherUser, ratingRel, targetUserMovies,
    collect(DISTINCT genre.name) AS overlappingGenres,
    collect(DISTINCT tag.name) AS overlappingTags,
    ratingRel.timestamp AS ratingTimestamp,
    {
        userId: otherUser.userId,
        fullName: otherUser.full_name,
        userRating: ratingRel.rating,
        ratedAt: ratingRel.timestamp
    } AS contributingUserData

// Collect movies rated by otherUser for intersection count
MATCH (otherUser)-[:RATED]->(otherUserRatedMovie:Movie)
WITH candidateMovie, jaccardSimilarity, overlappingGenres, overlappingTags, ratingTimestamp, targetUserMovies, otherUser, collect(otherUserRatedMovie) AS otherUserMovies, contributingUserData

WITH candidateMovie, jaccardSimilarity, size(overlappingGenres) AS genreScore, size(overlappingTags) AS tagScore,
    overlappingGenres, overlappingTags, ratingTimestamp, otherUser, targetUserMovies, otherUserMovies, contributingUserData,
    size(apoc.coll.intersection(targetUserMovies, otherUserMovies)) AS sharedRatedMoviesCount

WITH candidateMovie, jaccardSimilarity, genreScore, tagScore, overlappingGenres, overlappingTags, ratingTimestamp,
    duration.inDays(datetime(), datetime({epochMillis: ratingTimestamp * 1000})).days AS daysSinceRating,
    apoc.map.merge(contributingUserData, {sharedRatedMoviesCount: sharedRatedMoviesCount}) AS fullContributingUserData

WITH candidateMovie, jaccardSimilarity, genreScore, tagScore, overlappingGenres, overlappingTags, daysSinceRating,
    1.0 / (1 + daysSinceRating) AS recencyWeight,
    fullContributingUserData
ORDER BY fullContributingUserData.sharedRatedMoviesCount DESC
WITH candidateMovie, jaccardSimilarity, genreScore, tagScore, overlappingGenres, overlappingTags, daysSinceRating, recencyWeight,
    collect(fullContributingUserData) AS contributingUsersList

WITH candidateMovie,
    jaccardSimilarity * 1.5 + genreScore * 1.2 + tagScore + recencyWeight * 2 AS combinedHybridScore,
    overlappingGenres,
    overlappingTags,
    contributingUsersList

WITH candidateMovie.movieId AS movieId, candidateMovie.title AS movieTitle, combinedHybridScore,
    overlappingGenres,
    overlappingTags,
    contributingUsersList

ORDER BY combinedHybridScore DESC

WITH 
    movieId AS id, 
    movieTitle AS title, 
    max(combinedHybridScore) AS score,
    apoc.coll.toSet(apoc.coll.flatten(collect(overlappingGenres))) AS sharedGenres,
    apoc.coll.toSet(apoc.coll.flatten(collect(overlappingTags))) AS sharedTags,
    collect(contributingUsersList) AS rawContributors

UNWIND rawContributors AS userList
UNWIND userList AS contributor

WITH id, title, score, sharedGenres, sharedTags,
     contributor
ORDER BY contributor.sharedRatedMoviesCount DESC

WITH id, title, score, sharedGenres, sharedTags,
     collect(contributor) AS contributingUsers

RETURN 
    id, 
    title, 
    score, 
    sharedGenres, 
    sharedTags, 
    contributingUsers
ORDER BY score DESC
LIMIT 10
    """
    records = await query_neo4j(query, {"user_id": user_id})

    return [
    {
        key: record[key]
        for key in record.keys()
        if key not in ("contributingUsers", "sharedGenres", "sharedTags")
    }
    | {
        "totalSharedTags": len(record.get("sharedTags", [])),
        "totalSharedGenres": len(record.get("sharedGenres", [])),
        "totalContributingUsers": len(record.get("contributingUsers", [])),

        "top3ContributingUsers": [
            {
                **dict(contrib),
                "ratedAt": lib.format_timestamp(contrib.get("ratedAt")) if contrib.get("ratedAt") else None,
            }
            for contrib in record.get("contributingUsers", [])[:3]
        ],

        "top3SharedTags": record.get("sharedTags", [])[:3],
        "top3SharedGenres": record.get("sharedGenres", [])[:3],
    }
    for record in map(dict, records)
]
    




async def explain_recommendation(user_id: int, movie_id: int):
    duration_since_rating_expr = lib.cypher_duration_since_rating("r", "timestamp")

    query = f"""
    MATCH (targetUser:User {{userId: $user_id}}),
          (recommended:Movie {{movieId: $movie_id}})

    // Get movies targetUser rated
    MATCH (targetUser)-[:RATED]->(uMovie:Movie)
    WITH targetUser, recommended, collect(uMovie) AS userRatedMovies

    // Similar users and their rated movies
    MATCH (otherUser:User)-[:RATED]->(oMovie:Movie)
    WHERE targetUser <> otherUser
    WITH targetUser, recommended, userRatedMovies, otherUser, collect(oMovie) AS otherRatedMovies

    WITH targetUser, recommended, otherUser,
         apoc.coll.intersection(userRatedMovies, otherRatedMovies) AS shared,
         apoc.coll.union(userRatedMovies, otherRatedMovies) AS all
    WITH targetUser, recommended, otherUser, shared, all,
        CASE WHEN size(coalesce(all, [])) > 0 
            THEN size(coalesce(shared, [])) * 1.0 / size(coalesce(all, [])) 
            ELSE 0 END AS jaccard
    WHERE jaccard > 0.1

    // Check if other user rated the recommended movie
    MATCH (otherUser)-[r:RATED]->(recommended)

    // Find genres/tags overlapping
    OPTIONAL MATCH (targetUser)-[:RATED]->(:Movie)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(recommended)
    OPTIONAL MATCH (targetUser)-[:TAGGED]->(:Movie)-[:HAS_TAG]->(t:Tag)<-[:HAS_TAG]-(recommended)

    RETURN recommended.title AS recommendedTitle,
           collect(DISTINCT g.name) AS sharedGenres,
           collect(DISTINCT t.name) AS sharedTags,
           otherUser.full_name AS similarUser,
           r.rating AS similarUserRating,
           r.timestamp AS ratedAt,
           size(shared) AS sharedRatedMovies,
           jaccard,
           {duration_since_rating_expr}
    ORDER BY sharedRatedMovies DESC
    LIMIT 5
    """

    result = await query_neo4j(query, {"user_id": user_id, "movie_id": movie_id})

    explanations = []
    for row in result:
        duration = row.get("durationSinceRated", {})
        readable_duration = lib.format_duration(duration)

        text = (
            f"'{row['recommendedTitle']}' was recommended because user '{row['similarUser']}' "
            f"(Jaccard similarity: {row['jaccard']:.2f}) rated it {row['similarUserRating']} "
            f"{readable_duration} ago. You and they both rated {row['sharedRatedMovies']} similar movies."
        )
        if row["sharedGenres"]:
            text += f" It shares genres with your liked movies: {', '.join(row['sharedGenres'])}."
        if row["sharedTags"]:
            text += f" It also shares tags: {', '.join(row['sharedTags'])}."

        explanations.append({
            "text": text,
            "jaccard": row["jaccard"],
            "similarUser": row["similarUser"],
            "sharedGenres": row["sharedGenres"],
            "sharedTags": row["sharedTags"],
            "sharedRatedMovies": row["sharedRatedMovies"],
            "durationSinceRated": readable_duration,
        })

    return {
    "recommendedMovie": result[0]["recommendedTitle"],
    "reasons": explanations
}

