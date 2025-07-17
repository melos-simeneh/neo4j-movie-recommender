const BASE_URL = "http://localhost:3001";

export const getCollaborativeRecs = async (userId) => {
  const response = await fetch(`${BASE_URL}/recommend/collaborative/${userId}`);
  if (!response.ok)
    throw new Error("Failed to fetch collaborative recommendations");
  return response.json();
};

export const getContentBasedRecs = async (userId) => {
  const response = await fetch(`${BASE_URL}/recommend/content-based/${userId}`);
  if (!response.ok)
    throw new Error("Failed to fetch content-based recommendations");
  return response.json();
};

export const getContextBasedRecs = async (userId) => {
  const response = await fetch(`${BASE_URL}/recommend/context-based/${userId}`);
  if (!response.ok)
    throw new Error("Failed to fetch context-based recommendations");
  return response.json();
};

export const getHybridRecs = async (userId) => {
  const response = await fetch(`${BASE_URL}/recommend/hybrid/${userId}`);
  if (!response.ok) throw new Error("Failed to fetch hybrid recommendations");
  return response.json();
};

export const getExplanation = async (userId, movieId) => {
  const response = await fetch(`${BASE_URL}/explain/${userId}/${movieId}`);
  if (!response.ok) throw new Error("Failed to fetch explanation");
  return response.json();
};
