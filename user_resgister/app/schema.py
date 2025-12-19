from pydantic import BaseModel, Field, EmailStr, field_validator

# ---------- Request Model ----------
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, examples=["username123"])
    email: EmailStr
    password: str = Field(..., min_length=8, examples=["Strong@123"], max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if "password" in value.lower():
            raise ValueError("Password is too weak")
        return value

# ---------- Response Models ----------
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    password : str

class UserResponse(BaseModel):
    message: str
    user: UserOut
