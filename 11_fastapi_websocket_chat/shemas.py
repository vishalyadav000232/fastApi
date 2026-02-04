from pydantic import BaseModel

class Message(BaseModel):
    room: str
    sender: str
    content: str

class TokenData(BaseModel):
    username: str | None = None
