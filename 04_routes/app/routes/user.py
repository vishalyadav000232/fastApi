from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate ,UserResponse

router = APIRouter(
    prefix="/users",   # All routes start with /users
    tags=["Users"]     # Grouped under "Users" in Swagger
)

fake_db = []

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = {"id": len(fake_db) + 1, **user.dict()}
    fake_db.append(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def list_users():
    return fake_db
