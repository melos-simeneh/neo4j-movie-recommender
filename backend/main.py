from fastapi import FastAPI
from routes import auth_routes,recom_routes
from utils.neo4j_db import init_neo4j, close_neo4j
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Neo4j Recommendation System API",
    description="API for a graph-based movie recommendation system using Neo4j and MovieLens ml-latest-small dataset",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_neo4j()

@app.on_event("shutdown")
async def shutdown():
    await close_neo4j()
    
    
    
app.include_router(auth_routes.router)
app.include_router(recom_routes.router)
