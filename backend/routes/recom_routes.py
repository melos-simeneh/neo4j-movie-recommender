from fastapi import APIRouter, Query
from services import recom_service
from typing import List, Dict

router = APIRouter()

@router.get("/users", response_model=List[Dict])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    return await recom_service.get_all_users(page, page_size)

@router.get("/movies")
async def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    return await recom_service.get_all_movies(page, page_size)

@router.get("/recommend/collaborative/{user_id}", response_model=List[Dict])
async def recommend_collaborative(user_id: int):
    return await recom_service.collaborative_recommendation(user_id)

@router.get("/recommend/content-based/{user_id}", response_model=List[Dict])
async def recommend_content(user_id: int):
    return await recom_service.content_based_recommendation(user_id)

@router.get("/recommend/context-based/{user_id}", response_model=List[Dict])
async def recommend_context(user_id: int):
    return await recom_service.context_based_recommendation(user_id)

@router.get("/recommend/hybrid/{user_id}", response_model=List[Dict])
async def recommend_hybrid(user_id: int):
    return await recom_service.hybrid_recommendation(user_id)


@router.get("/explain/{user_id}/{movie_id}")
async def explain_recommendation(user_id: int, movie_id: int):
    return await recom_service.explain_recommendation(user_id,movie_id)
