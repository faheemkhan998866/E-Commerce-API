from fastapi import APIRouter
from models_user import User,LoginUser
from database import users_collection
from security import hash_password, verify_password

router = APIRouter()


@router.post("/register")
def register_user(user: User):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if existing_user:
        return {
            "message": "User already exists"
        }

    hashed_password = hash_password(user.password)

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login_user(user: LoginUser):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    password_correct = verify_password(
        user.password,
        existing_user["password"]
    )

    if not password_correct:
        return {
            "message": "Invalid email or password"
        }

    return {
        "message": "Login successful"
    }