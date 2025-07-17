// src/components/ExplanationModal.jsx
export default function ExplanationModal({
  userId,
  movieId,
  movieData,
  explanationData,
  isLoading,
  error,
  onClose,
}) {
  return (
    <div className="modal modal-open">
      <div className="modal-box max-w-3xl">
        <h3 className="font-bold text-lg mb-4">
          Explanation for {movieData?.title}
        </h3>

        {isLoading && (
          <div className="flex justify-center my-8">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        )}

        {error && (
          <div className="alert alert-error mb-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {explanationData && (
          <div className="space-y-4">
            <h4 className="font-semibold">Recommendation Reasons:</h4>
            <ul className="space-y-3">
              {explanationData.reasons.map((reason, index) => (
                <li key={index} className="bg-base-200 p-3 rounded-lg">
                  <p>{reason.text}</p>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {reason.sharedGenres?.map((genre) => (
                      <span key={genre} className="badge badge-primary">
                        {genre}
                      </span>
                    ))}
                    {reason.sharedTags?.map((tag) => (
                      <span key={tag} className="badge badge-secondary">
                        {tag}
                      </span>
                    ))}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="modal-action">
          <button onClick={onClose} className="btn">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
