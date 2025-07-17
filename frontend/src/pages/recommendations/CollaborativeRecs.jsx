// src/pages/recommendations/CollaborativeRecs.jsx
import { useQuery } from "@tanstack/react-query";
import RecommendationCard from "../../components/RecommendationCard";
import RecommendationCardSkeleton from "../../components/RecommendationCardSkeleton";
import { getCollaborativeRecs } from "../../api/recommendations";
import { useAuth } from "../../context/AuthContext";

const getPosterUrl = (tmdbId) => {
  return tmdbId
    ? `https://image.tmdb.org/t/p/w500/${tmdbId}`
    : "/placeholder-poster.jpg";
};

export default function CollaborativeRecs() {
  const { user } = useAuth();
  const userId = user?.userId;

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["collaborativeRecs", userId],
    queryFn: () => getCollaborativeRecs(userId),
  });

  if (isLoading) {
    return (
      <div className="p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">
            {" "}
            Top {data?.length} Collaborative Recommendations
          </h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, index) => (
            <RecommendationCardSkeleton key={index} />
          ))}
        </div>
      </div>
    );
  }

  if (isError) {
    console.error("Error fetching collaborative recommendations:", error);
    return (
      <div className="alert alert-error">
        Error: {error.message || "Failed to load recommendations"}
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="alert alert-warning">
        No collaborative recommendations available for this user
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Collaborative Recommendations</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((rec) => (
          <RecommendationCard
            key={rec.movieId}
            movie={{
              movieId: rec.movieId,
              title: rec.title,
              score: rec.score,
              totalSimilarUsersWhoRated: rec.totalSimilarUsersWhoRated,
              topContributors: rec.top5Recommenders.map((r) => ({
                userId: r.userId,
                name: r.full_name,
                rating: r.rating,
              })),
              posterUrl: getPosterUrl(rec.tmdbId),
            }}
            showExplain={false} // Disable explain button for collaborative
          />
        ))}
      </div>
    </div>
  );
}
