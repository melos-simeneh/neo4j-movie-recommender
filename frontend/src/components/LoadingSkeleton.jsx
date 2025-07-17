export default function LoadingSkeleton({ count }) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {[...Array(count)].map((_, i) => (
          <div key={i} className="card bg-base-200 dark:bg-gray-800 shadow-xl">
            <div className="aspect-[2/3] bg-gray-300 dark:bg-gray-700 rounded-t-xl animate-pulse" />
            <div className="card-body p-4 space-y-3">
              <div className="h-6 bg-gray-300 dark:bg-gray-700 rounded animate-pulse" />
              <div className="flex gap-2">
                <div className="h-4 w-16 bg-gray-300 dark:bg-gray-700 rounded animate-pulse" />
                <div className="h-4 w-16 bg-gray-300 dark:bg-gray-700 rounded animate-pulse" />
              </div>
              <div className="h-8 mt-2 bg-gray-300 dark:bg-gray-700 rounded animate-pulse" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
