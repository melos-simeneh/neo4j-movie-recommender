# 🎬 Neo4j Movie Recommendation System

A full-stack movie recommendation system powered by **Neo4j**, with a **FastAPI** backend and a **React** frontend. It uses the [MovieLens (ml-latest-small)](https://grouplens.org/datasets/movielens/latest/) dataset to deliver personalized recommendations using collaborative, content-based, context-aware, and hybrid filtering techniques.

## 🧠 Features

- Four recommendation strategies (collaborative, content, context, hybrid)

- Recommendation explanations

- REST API with interactive docs

- Neo4j schema constraints, indexes, and initial data loading

## 📁 Project Structure

neo4j-movie-recommender
├── backend/ # FastAPI backend for recommendation APIs
├── frontend/ # React frontend UI
├── dataset/ # MovieLens dataset (movies.csv, ratings.csv etc.)
├── db/ # Neo4j Docker Compose config and init scripts
└── README.md # Project overview

## 🚀 Tech Stack

| Component      | Tech        |
|----------------|-------------|
| Backend        | FastAPI, Python 3.10+ |
| Frontend       | React (JavaScript) |
| Database       | Neo4j (via Docker Compose) |
| Dataset        | MovieLens (ml-latest-small) |

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/melos-simeneh/neo4j-movie-recommender.git
cd neo4j-movie-recommender
```

### 2. Set Up Neo4j (Database)

Navigate to the db/ folder and start the Neo4j container:

```bash
cd db
docker-compose up -d
```

- The dataset will be loaded automatically via `init.cypher`
- Access Neo4j browser at [http://localhost:7474](http://localhost:7474)
- Default credentials: `neo4j / Test@1234`

### 3. Run the Backend (FastAPI)

In a new terminal:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload  --port 3000
```

API Docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run the Frontend (React)

If frontend is set up:

```bash
cd frontend
npm install
npm start
```

- Visit: [http://localhost:3000](http://localhost:3000)

## 📡 API Features

- `POST /login` – Authenticate a user

- `GET /users` – List users

- `GET /movies` – List movies

- `GET /recommend/collaborative/{user_id}` – Collaborative filtering

- `GET /recommend/content-based/{user_id}` – Content-based filtering

- `GET /recommend/context-based/{user_id}` – Context-aware recommendation

- `GET /recommend/hybrid/{user_id}` – Hybrid recommendation

- `GET /explain/{user_id}/{movie_id}` – Explain why a movie was recommended

## 🗃 Dataset

Using the `ml-latest-small version` of MovieLens, which includes:

- `movies.csv`

- `ratings.csv`

- `tags.csv`

- `links.csv`

In addition, a `users.csv` file was generated using a Python script located at:

`backend/utils/generate_users_csv.py`
This script generates mock user profiles for existing user IDs.

## 👨‍💻 Author

Built with 💚 by **`Melos`**
