// src/pages/recommendations/ContextBasedRecs.jsx
import { useQuery } from "@tanstack/react-query";
import RecommendationCard from "../../components/RecommendationCard";
import RecommendationCardSkeleton from "../../components/RecommendationCardSkeleton";
import { getContextBasedRecs } from "../../api/recommendations";
import { useAuth } from "../../context/AuthContext";

const getMovieImage = () => {
  const randomId = Math.floor(Math.random() * 1000);
  return `https://picsum.photos/id/${randomId}/500/750`;
};

export default function ContextBasedRecs() {
  const { user } = useAuth();
  const userId = user?.userId;

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["contextBasedRecs", userId],
    queryFn: () => getContextBasedRecs(userId),
  });

  if (isLoading) {
    return (
      <div className="p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Context-Based Recommendations</h1>
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
    console.error("Error fetching context-based recommendations:", error);
    return (
      <div className="alert alert-error">
        Error: {error.message || "Failed to load recommendations"}
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="alert alert-warning">
        No context-based recommendations available for this user
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">
          {" "}
          Top {data?.length} Context-Based Recommendations
        </h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((rec) => (
          <RecommendationCard
            key={rec.movieId}
            movie={{
              movieId: rec.movieId,
              title: rec.title,
              score: rec.weightedScore,
              averageRating: rec.averageRating,
              numRatings: rec.numRatings,
              latestRatingDate: rec.latestRatingDate,
              recentRaters: rec.recentRaters,
              posterUrl: getMovieImage(rec.tmdbId),
            }}
            showExplain={false} // Disable explain button for context-based
          />
        ))}
      </div>
    </div>
  );
}
