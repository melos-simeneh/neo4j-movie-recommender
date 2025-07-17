// src/components/RecommendationStats.jsx
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

const RecommendationStats = ({ title, value, icon, link }) => {
  const content = (
    <div className="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow">
      <div className="card-body">
        <div className="flex items-center">
          <div className="p-3 rounded-full bg-primary bg-opacity-20 text-primary">
            {icon}
          </div>
          <div className="ml-4">
            <h3 className="text-lg font-semibold">{title}</h3>
            <p className="text-2xl font-bold">{value}</p>
          </div>
        </div>
      </div>
    </div>
  );

  return link ? (
    <Link to={link} className="block">
      {content}
    </Link>
  ) : (
    content
  );
};

RecommendationStats.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.element.isRequired,
  link: PropTypes.string,
};

export default RecommendationStats;
