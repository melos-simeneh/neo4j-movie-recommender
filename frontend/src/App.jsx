import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Outlet,
  useNavigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./context/AuthContext";
import { useAuth } from "./context/AuthContext";
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import CollaborativeRecs from "./pages/recommendations/CollaborativeRecs";
import ContentBasedRecs from "./pages/recommendations/ContentBasedRecs";
import ContextBasedRecs from "./pages/recommendations/ContextBasedRecs";
import HybridRecs from "./pages/recommendations/HybridRecs";
import { useEffect } from "react";

const queryClient = new QueryClient();

const AppWrapper = () => {
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <AppRoutes />
        </Router>
      </QueryClientProvider>
    </AuthProvider>
  );
};

const ProtectedLayout = () => {
  const { user } = useAuth();

  return (
    <Layout>
      <Outlet context={{ userId: user?.userId }} />
    </Layout>
  );
};

const RequireAuth = ({ children }) => {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !user) {
      navigate("/login", { replace: true });
    }
  }, [user, isLoading, navigate]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  return user ? children : null;
};

function AppRoutes() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected routes */}
      <Route
        element={
          <RequireAuth>
            <ProtectedLayout />
          </RequireAuth>
        }
      >
        <Route path="/" element={<HybridRecs />} />
        <Route
          path="/recommend/collaborative"
          element={<CollaborativeRecs />}
        />
        <Route path="/recommend/content-based" element={<ContentBasedRecs />} />
        <Route path="/recommend/context-based" element={<ContextBasedRecs />} />
        <Route path="/recommend/hybrid" element={<HybridRecs />} />
      </Route>

      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default AppWrapper;
