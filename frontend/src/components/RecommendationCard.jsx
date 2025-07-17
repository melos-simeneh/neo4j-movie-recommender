// src/components/RecommendationCard.jsx
import { FaInfoCircle, FaStar } from "react-icons/fa";

export default function RecommendationCard({
  movie,
  showExplain = true,
  onExplain,
}) {
  const formatScore = (score) => {
    if (score === undefined || score === null) return null;

    // If score is very small (scientific notation)
    if (Math.abs(score) < 0.001) {
      return score.toExponential(2); // Shows as 5.65e-10
    }

    // For regular scores
    return Math.round(score * 100) + "%";
  };
  return (
    <div className="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow">
      <figure>
        <img
          src={movie.posterUrl}
          alt={`Poster for ${movie.title}`}
          className="w-full h-64 object-cover"
          onError={(e) => {
            e.target.src = "/placeholder-poster.jpg";
          }}
        />
      </figure>
      <div className="card-body">
        <h2 className="card-title">
          {movie.title}{" "}
          {movie.score && (
            <div className="badge badge-primary ml-2">
              {formatScore(movie.score)}
            </div>
          )}
        </h2>

        {movie.sharedGenres && (
          <div className="flex flex-wrap gap-1">
            {movie.sharedGenres.slice(0, 3).map((genre) => (
              <div key={genre} className="badge badge-outline">
                {genre}
              </div>
            ))}
          </div>
        )}

        {movie.totalSimilarUsersWhoRated && (
          <div className="flex items-center text-sm">
            <FaStar className="text-yellow-400 mr-1" />
            <span>
              Liked by {movie.totalSimilarUsersWhoRated} similar users
            </span>
          </div>
        )}

        {showExplain && (
          <div className="card-actions justify-between mt-4">
            <button onClick={onExplain} className="btn btn-sm btn-ghost">
              <FaInfoCircle className="mr-1" />
              Explain
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
