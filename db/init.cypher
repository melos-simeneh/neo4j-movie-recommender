// ==========================
// MovieLens Neo4j Setup
// Dataset: ml-latest-small
// ==========================

// --- 1. Clean Database ---
MATCH (n) DETACH DELETE n;

// --- 2. Constraints for Uniqueness ---
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.userId IS UNIQUE;
CREATE CONSTRAINT movie_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.movieId IS UNIQUE;
CREATE CONSTRAINT genre_name IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE;
CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE;

// --- 3. Indexes for Performance ---
CREATE INDEX rating_index IF NOT EXISTS FOR ()-[r:RATED]-() ON (r.rating);
CREATE INDEX rated_timestamp_index IF NOT EXISTS FOR ()-[r:RATED]-() ON (r.timestamp);
CREATE INDEX tagged_timestamp_index IF NOT EXISTS FOR ()-[r:TAGGED]-() ON (r.timestamp);

// --- 4. Load Users ---
LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row
WITH row
WHERE row.userId IS NOT NULL
MERGE (u:User {userId: toInteger(row.userId)})
SET u.username = row.username,
    u.full_name = row.full_name,
    u.password = row.password;

// --- 5. Load Movies ---
LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
WITH row
WHERE row.movieId IS NOT NULL
MERGE (m:Movie {movieId: toInteger(row.movieId)})
SET m.title = row.title,
    m.genres = row.genres;

// --- 6. Load Genres from Movies ---
LOAD CSV WITH HEADERS FROM 'file:///movies.csv' AS row
WITH row, split(row.genres, '|') AS genres
MATCH (m:Movie {movieId: toInteger(row.movieId)})
UNWIND genres AS genre
WITH m, trim(genre) AS genreName
WHERE genreName <> ""
MERGE (g:Genre {name: genreName})
MERGE (m)-[:HAS_GENRE]->(g);

// --- 7. Load Ratings ---
LOAD CSV WITH HEADERS FROM 'file:///ratings.csv' AS row
WITH row, toInteger(row.userId) AS uid, toInteger(row.movieId) AS mid
MATCH (u:User {userId: uid})
MATCH (m:Movie {movieId: mid})
MERGE (u)-[r:RATED]->(m)
SET r.rating = toFloat(row.rating),
    r.timestamp = toInteger(row.timestamp);

// --- 8. Load Tags (User → Tag and Movie → Tag) ---
LOAD CSV WITH HEADERS FROM 'file:///tags.csv' AS row
WITH row
WHERE row.tag IS NOT NULL AND trim(row.tag) <> ""
WITH row, toInteger(row.userId) AS uid, toInteger(row.movieId) AS mid, trim(row.tag) AS tagName
MATCH (u:User {userId: uid})
MATCH (m:Movie {movieId: mid})
MERGE (t:Tag {name: tagName})
MERGE (u)-[r:TAGGED]->(t)
SET r.timestamp = toInteger(row.timestamp)
MERGE (m)-[:HAS_TAG]->(t);

// --- 9. Load IMDb and TMDb IDs ---
LOAD CSV WITH HEADERS FROM 'file:///links.csv' AS row
WITH row
MATCH (m:Movie {movieId: toInteger(row.movieId)})
SET m.imdbId = row.imdbId,
    m.tmdbId = row.tmdbId;
