import {
  FaUserCircle,
  FaUserFriends,
  FaTags,
  FaCalendarAlt,
  FaRandom,
} from "react-icons/fa";
import { GiFilmSpool } from "react-icons/gi";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../context/AuthContext"; // ✅ Import auth context

export default function Navbar() {
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const { user, logout } = useAuth(); // ✅ Destructure user and logout

  return (
    <header className="navbar bg-base-100 shadow-sm sticky top-0 z-50">
      {/* Logo/Brand */}
      <div className="flex-1">
        <Link
          to="/"
          className="btn btn-ghost normal-case text-xl hover:bg-transparent px-2"
        >
          <GiFilmSpool className="text-primary text-2xl mr-2" />
          <span className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            MovieRecs
          </span>
        </Link>
      </div>

      {/* Desktop Navigation */}
      <div className="flex flex-1 justify-center">
        <ul className="menu menu-horizontal px-1 gap-1">
          <li>
            <Link to="/recommend/hybrid" className="font-medium">
              <FaRandom className="text-lg mr-2 text-warning" />
              Hybrid
            </Link>
          </li>
          <li>
            <Link to="/recommend/collaborative" className="font-medium">
              <FaUserFriends className="text-lg mr-2 text-accent" />
              Collaborative
            </Link>
          </li>
          <li>
            <Link to="/recommend/content-based" className="font-medium">
              <FaTags className="text-lg mr-2 text-info" />
              Content-Based
            </Link>
          </li>
          <li>
            <Link to="/recommend/context-based" className="font-medium">
              <FaCalendarAlt className="text-lg mr-2 text-success" />
              Context-Based
            </Link>
          </li>
        </ul>
      </div>

      {/* Right side user menu */}
      <div className="flex-none">
        <div className="dropdown dropdown-end">
          <button
            className="btn btn-ghost btn-circle avatar"
            onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
          >
            <div className="w-10 h-10 rounded-full grid place-items-center">
              <FaUserCircle className="text-4xl" />
            </div>
          </button>
          <ul
            tabIndex={0}
            className={`dropdown-content mt-3 z-[1] p-2 shadow menu menu-sm bg-base-100 rounded-box w-52 ${
              isUserMenuOpen ? "block" : "hidden"
            }`}
          >
            {user && (
              <p className="px-2 py-1 text-sm text-gray-500">
                <strong>{user.full_name}</strong>
              </p>
            )}
            <li>
              <button onClick={logout} className="text-error font-semibold">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </header>
  );
}
