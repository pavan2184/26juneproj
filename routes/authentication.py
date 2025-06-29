from fastapi import APIRouter, HTTPException
from models import UserRegister, hash_password, verify_password
from database import users_collection
from jwttoken import create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginModel(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "password": hash_password(user.password)
    }
    users_collection.insert_one(user_data)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(user: LoginModel):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(db_user["_id"])
    token = create_access_token(data={"sub": user.email, "user_id": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer", "user_id": user_id}
