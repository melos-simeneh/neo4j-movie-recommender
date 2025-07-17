export default function RecommendationCardSkeleton() {
  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="skeleton h-64 w-full"></div>
      <div className="card-body space-y-3">
        <div className="flex justify-between items-center">
          <div className="skeleton h-6 w-3/4"></div>
          <div className="skeleton h-6 w-10"></div>
        </div>

        <div className="flex gap-2">
          <div className="skeleton h-4 w-16"></div>
          <div className="skeleton h-4 w-16"></div>
          <div className="skeleton h-4 w-16"></div>
        </div>

        <div className="flex items-center">
          <div className="skeleton h-4 w-4 rounded-full mr-2"></div>
          <div className="skeleton h-4 w-32"></div>
        </div>

        <div className="card-actions justify-end">
          <div className="skeleton h-8 w-20"></div>
        </div>
      </div>
    </div>
  );
}
