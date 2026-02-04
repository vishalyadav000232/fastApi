# from fastapi import FastAPI, Request, HTTPException
# # from slowapi import Limiter, _rate_limit_exceeded_handler  # Old slowapi approach (kept for reference)
# # from slowapi.util import get_remote_address
# import time

# app = FastAPI()

# '''
# Old slowapi setup (commented out):
# # limiter = Limiter(key_func=get_remote_address)
# # app.state.limiter = limiter
# # app.add_exception_handler(429, _rate_limit_exceeded_handler)
# '''

# # =========================
# # Custom Middleware Rate Limiter
# # =========================

# # Dictionary to track requests per IP
# request_log = {}

# LIMIT = 5   # Maximum requests per window
# WINDOW = 60  # Time window in seconds

# @app.middleware("http")
# async def limit_request(request: Request, call_next):
#     """
#     Middleware to limit requests per client IP.
#     Raises HTTP 429 if the client exceeds the rate limit.
#     """
#     ip = request.client.host
#     now = time.time()

#     # Get existing requests for this IP and remove old ones outside the window
#     request_times = request_log.get(ip, [])
#     request_times = [t for t in request_times if now - t < WINDOW]

#     # Check if limit exceeded
#     if len(request_times) >= LIMIT:
#         raise HTTPException(status_code=429, detail="Too many requests")

#     # Log the current request
#     request_times.append(now)
#     request_log[ip] = request_times

#     # Proceed to the endpoint
#     return await call_next(request)


# # =========================
# # API Endpoints
# # =========================

# @app.get("/")
# async def home(request: Request):
#     """
#     Home endpoint with rate limiting applied via middleware.
#     """
#     return {"message": "Hello, FastAPI with rate limiting!"}

# '''
# Optional slowapi decorator approach (if you want per-route limits):

# @app.get("/slowapi")
# @limiter.limit("2/minute")  # max 2 requests per minute per IP
# async def slowapi_example(request: Request):
#     return {"message": "This endpoint uses slowapi rate limiting!"}
# '''



# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import APIKeyHeader ,APIKeyQuery

# app = FastAPI()

# api_key_scheme = APIKeyHeader(name="x-key",auto_error=False)

# VALID_KEYS = {"admin123", "service999"}

# def verify_api_key(api_key: str = Depends(api_key_scheme)):
#     if api_key not in VALID_KEYS:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid API Key"
#         )
#     return api_key

# @app.get("/items")
# def get_items(api_key: str = Depends(verify_api_key)):
#     return {"msg": "Access granted", "key": api_key}

# query_scheme = APIKeyQuery(name="api_key")


# def verify_key(api_key: str = Depends(query_scheme)):
#     if api_key not in VALID_KEYS:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid API Key"
#         )
#     return api_key

# @app.get("/secure-items")
# def secure_items(api_key: str = Depends(verify_key)):
#     return {"msg": "Access granted", "key": api_key}



# from typing import Annotated
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# import secrets

# app = FastAPI()
# security = HTTPBasic()

# def verify_basic_auth(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)]
# ):
#     correct_username = "admin"
#     correct_password = "admin123"

#     # secrets.compare_digest timing attack se bachata hai
#     is_user_ok = secrets.compare_digest(credentials.username, correct_username)
#     is_pass_ok = secrets.compare_digest(credentials.password, correct_password)

#     if not (is_user_ok and is_pass_ok):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"},
#         )

#     return credentials.username

# @app.get("/admin")
# def admin_panel(username: str = Depends(verify_basic_auth)):
#     return {"msg": f"Welcome {username}"}




# from fastapi import FastAPI, Depends
# from fastapi.security import OAuth2AuthorizationCodeBearer

# app = FastAPI()

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
#     tokenUrl="https://oauth2.googleapis.com/token",
# )

# @app.get("/me")
# def me(token: str = Depends(oauth2_scheme)):
#     return {"token": token}







# from fastapi import FastAPI, Depends, HTTPException, status, Security
# from fastapi.security import OAuth2PasswordBearer, SecurityScopes
# from jose import jwt, JWTError
# from passlib.context import CryptContext
# from pydantic import BaseModel
# from typing import Optional, List

# # ---------------- CONFIG ----------------
# SECRET_KEY = "MY_SUPER_SECRET_KEY"
# ALGORITHM = "HS256"

# app = FastAPI()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # OAuth2PasswordBearer me scopes define karte hain
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token",
#     scopes={
#         "user": "Normal user access",
#         "admin": "Admin access"
#     }
# )

# # ---------------- DUMMY USERS DB ----------------
# fake_users_db = {
#     "vishal": {
#         "username": "vishal",
#         "hashed_password": pwd_context.hash("1234"),
#         "scopes": ["user"]
#     },
#     "admin": {
#         "username": "admin",
#         "hashed_password": pwd_context.hash("admin123"),
#         "scopes": ["admin"]
#     }
# }

# # ---------------- MODELS ----------------
# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class User(BaseModel):
#     username: str
#     scopes: List[str] = []

# # ---------------- UTILS ----------------
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def authenticate_user(username: str, password: str):
#     user = fake_users_db.get(username)
#     if not user:
#         return None
#     if not verify_password(password, user["hashed_password"]):
#         return None
#     return user

# def create_access_token(data: dict):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# # ---------------- TOKEN API ----------------
# from fastapi.security import OAuth2PasswordRequestForm

# @app.post("/token", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password"
#         )

#     token_data = {
#         "sub": user["username"],
#         "scopes": user["scopes"]
#     }

#     access_token = create_access_token(token_data)

#     return {"access_token": access_token, "token_type": "bearer"}

# # ---------------- SECURITY + SCOPES CHECK ----------------
# def get_current_user(
#     security_scopes: SecurityScopes,
#     token: str = Depends(oauth2_scheme)
# ):
#     """
#     security_scopes.scopes = route pe required scopes
#     token se user scopes decode karke match karenge
#     """

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid token or not authenticated",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: Optional[str] = payload.get("sub")
#         token_scopes: List[str] = payload.get("scopes", [])

#         if username is None:
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception

#     # user fetch
#     user_data = fake_users_db.get(username)
#     if not user_data:
#         raise credentials_exception

#     # ✅ IMPORTANT: scopes check
#     for scope in security_scopes.scopes:
#         if scope not in token_scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Not enough permissions. Required scope: {scope}",
#             )

#     return User(username=username, scopes=token_scopes)

# # ---------------- ROUTES ----------------

# # ✅ Any logged-in user (no special scope required)
# @app.get("/profile")
# def profile(user: User = Security(get_current_user, scopes=[])):
#     return {
#         "msg": "Welcome user",
#         "username": user.username,
#         "scopes": user.scopes
#     }

# # ✅ Only admin can access
# @app.get("/admin")
# def admin_panel(user: User = Security(get_current_user, scopes=["admin"])):
#     return {
#         "msg": "Welcome Admin",
#         "username": user.username,
#         "scopes": user.scopes
#     }

# # ✅ Only normal user can access
# @app.get("/user-area")
# def user_area(user: User = Security(get_current_user, scopes=["user"])):
#     return {
#         "msg": "Welcome User Area",
#         "username": user.username,
#         "scopes": user.scopes
#     }
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me domain set karna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Connection Manager (Broadcast)
# -----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # websocket handshake accept
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()

# -----------------------------
# Dummy Seats (in-memory data)
# -----------------------------
seats = [
    {"seat_id": 1, "status": "free"},
    {"seat_id": 2, "status": "free"},
    {"seat_id": 3, "status": "occupied"},
    {"seat_id": 4, "status": "free"},
]


@app.get("/")
def root():
    return {"message": "FastAPI WebSocket Server Running ✅"}


@app.get("/seats")
def get_seats():
    return {"seats": seats}


# -----------------------------
# WebSocket Endpoint
# -----------------------------
@app.websocket("/ws/seats")
async def ws_seats(websocket: WebSocket):
    await manager.connect(websocket)

    # client connect hote hi initial data send karo
    await manager.send_personal_message(websocket, {
        "type": "initial_data",
        "seats": seats
    })

    try:
        while True:
            # receive from client
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Example payload:
            # { "type": "update_seat", "seat_id": 2, "status": "occupied" }

            if payload.get("type") == "update_seat":
                seat_id = payload.get("seat_id")
                new_status = payload.get("status")

                # update seat
                for seat in seats:
                    if seat["seat_id"] == seat_id:
                        seat["status"] = new_status

                # broadcast updated seats to all clients
                await manager.broadcast({
                    "type": "seat_update",
                    "seats": seats
                })

            else:
                # unknown message type
                await manager.send_personal_message(websocket, {
                    "type": "error",
                    "message": "Unknown message type"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected ❌")
