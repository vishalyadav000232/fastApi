from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt

# ---------------------
# CONFIG
# ---------------------
SECRET_KEY = "wZ1k9QxL_6pVn1sJf8uT2c-K9aQHfP0rGgX5L3YbVq8="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# ---------------------
# APP INIT
# ---------------------
app = FastAPI(title="Security FastAPI Example")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------------------
# UTILITY FUNCTIONS
# ---------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return username
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# ---------------------
# ROUTES
# ---------------------

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Security FastAPI server is running on port 8000"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simple hardcoded user check
    if form_data.username == "admin" and form_data.password == "1234":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )


@app.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    return {"msg": f"Tum andar aa gaye, {username}", "token": token}
