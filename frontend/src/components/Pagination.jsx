// src/components/Pagination.jsx
export default function Pagination({
  currentPage,
  totalItems,
  itemsPerPage,
  onPageChange,
}) {
  const totalPages = Math.ceil(totalItems / itemsPerPage);

  return (
    <div className="join mt-6">
      <button
        className="join-item btn"
        onClick={() => onPageChange(Math.max(1, currentPage - 1))}
        disabled={currentPage === 1}
      >
        «
      </button>
      <button className="join-item btn">Page {currentPage}</button>
      <button
        className="join-item btn"
        onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
        disabled={currentPage === totalPages}
      >
        »
      </button>
    </div>
  );
}
