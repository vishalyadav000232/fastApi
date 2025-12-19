from fastapi import FastAPI, status # type: ignore
from app.schema import UserRegister, UserResponse ,UserLogin ,LoginResponse
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


@app.post("/login", status_code=200, response_model=LoginResponse)
def login(user: UserLogin):
    # 🔹 Dummy check (later this will be DB + hashed password)
    if user.email != "user@gmail.com" or user.password != "User@123":
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful"
    }