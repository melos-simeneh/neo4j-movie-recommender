from fastapi import APIRouter, HTTPException
from schemas.auth_schemas import LoginRequest
from services.auth_services import get_user

router = APIRouter()

@router.post("/login")
async def login_user(request: LoginRequest): 
    user = await get_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "user": user}
