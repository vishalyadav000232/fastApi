from fastapi import FastAPI
from app.routes.user import router as user_router





app = FastAPI()

@app.get("/")
async def home():
    return {
        "message": "home data"
    }

app.include_router(user_router)