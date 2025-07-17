// src/pages/recommendations/HybridRecs.jsx
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import RecommendationCard from "../../components/RecommendationCard";
import RecommendationCardSkeleton from "../../components/RecommendationCardSkeleton";
import ExplanationModal from "../../components/ExplanationModal";
import { getHybridRecs, getExplanation } from "../../api/recommendations";
import { useAuth } from "../../context/AuthContext";

const getMovieImage = () => {
  const randomId = Math.floor(Math.random() * 1000);
  return `https://picsum.photos/id/${randomId}/500/750`;
};

export default function HybridRecs() {
  const { user } = useAuth();
  const userId = user?.userId;
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [explanationData, setExplanationData] = useState(null);
  const [isExplanationLoading, setIsExplanationLoading] = useState(false);
  const [explanationError, setExplanationError] = useState(null);

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["hybridRecs", userId],
    queryFn: () => getHybridRecs(userId),
  });

  const handleExplain = async (movieId) => {
    setSelectedMovie(movieId);
    setIsExplanationLoading(true);
    setExplanationError(null);

    try {
      const explanation = await getExplanation(userId, movieId);
      setExplanationData(explanation);
    } catch (err) {
      console.error("Error fetching explanation:", err);
      setExplanationError(err.message);
    } finally {
      setIsExplanationLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Hybrid Recommendations</h1>
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
    console.error("Error fetching hybrid recommendations:", error);
    return (
      <div className="alert alert-error">
        Error: {error.message || "Failed to load recommendations"}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="alert alert-warning">No recommendations available</div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">
          Top {data?.length} Hybrid Recommendations
        </h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((rec) => (
          <RecommendationCard
            key={rec.id}
            movie={{
              movieId: rec.id,
              title: rec.title,
              score: rec.score,
              sharedGenres: rec.top3SharedGenres || [],
              sharedTags: rec.top3SharedTags || [],
              totalSimilarUsersWhoRated: rec.totalContributingUsers || 0,
              topContributors: rec.top3ContributingUsers || [],
              posterUrl: getMovieImage(),
            }}
            onExplain={() => handleExplain(rec.id)}
            showExplain={false}
          />
        ))}
      </div>

      {selectedMovie && (
        <ExplanationModal
          userId={userId}
          movieId={selectedMovie}
          movieData={data.find((movie) => movie.id === selectedMovie)}
          explanationData={explanationData}
          isLoading={isExplanationLoading}
          error={explanationError}
          onClose={() => {
            setSelectedMovie(null);
            setExplanationData(null);
            setExplanationError(null);
          }}
        />
      )}
    </div>
  );
}
