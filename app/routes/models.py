from pydantic import BaseModel, Field, EmailStr, field_validator
import re
import bcrypt
from fastapi import APIRouter

router = APIRouter()

class UserRegister(BaseModel):

    name : str
    age : int  = Field(...,ge=18, le=120)
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, pw):
    
        if len(pw) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"\d", pw):
            raise ValueError("Password must include a digit")
        if not re.search(r"[@$!%*?&]", pw):
            raise ValueError("Password must include a special character (@$!%*?&)")
        if not re.search(r"[A-Z]", pw):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r"[a-z]", pw):
            raise ValueError("Password must include a lowercase letter")
        return pw
    

def hash_password(password: str):
        pw_bytes = str(password).encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(pw_bytes, salt)
        return hash.decode('utf-8')
    
def verify_password(plain: str, hashed: str) :
    user_bytes = plain.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')  
    return bcrypt.checkpw(user_bytes, hashed_bytes)


@router.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):     #linked to where database is
        return {"msg": "User exists"}
    
    user_data = {
        "email": user.email,
        "password": hash_password(user.password)  
    }
    users_collection.insert_one(user_data)                  #linked to where database is
    return {"msg": "User registered successfully"}