from fastapi import FastAPI, status # type: ignore
from app.schema import UserRegister, UserResponse
from app.security import hash_password  
app = FastAPI()

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    hashed_pass = hash_password(user.password)
    new_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "password": hashed_pass  
    }

    return {
        "message": "User created successfully ✅",
        "user":  new_user
        
    }
