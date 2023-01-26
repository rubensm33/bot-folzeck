import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class user (BaseModel):
    name: str
    lastname: str
    user_id: Optional[str] = uuid4().hex
    genre: Literal["Male", "Female"]

USER_DATABASE = []


USERS_FILE = "users.json"


if os.path.exists(USERS_FILE):
    with open (USERS_FILE, "r") as file:
        USER_DATABASE = json.load(file)


##/ -> Root to apresentation 

@app.get("/")
async def home():
    return {"message":"Folzeck Group"}

# /list-users -> List all users
@app.get("/list-users")
async def list_users():
    return { "users": USER_DATABASE }


# /list-user-by-index/{index} -> List User by Index
@app.get("/list-user-by-index/{index}")
async def list_user_by_index(index: int):
    if index < 0 or index >= len(USER_DATABASE):
        raise HTTPException(404, "Index out of range")
    else:
        return { "users": USER_DATABASE[index] }



# /add-user -> Add New User
@app.post("/add-user")
async def add_user(user: user):
    user.user_id = uuid4().hex
    json_user = jsonable_encoder(user)
    USER_DATABASE.append(json_user)
    
    with open (USERS_FILE, "w") as file:
        json.dump(USER_DATABASE, file)
    return { "message": f'The user {user} has been added' }



# /delete-user-by-index/{index} -> Delete User by Index
@app.delete("/delete-user-by-index/{index}")
async def delete_user_by_index(index: int):
    user.user_id = uuid4().hex
    json_user = jsonable_encoder(user)
    USER_DATABASE.pop(json_user)
    
    with open (USERS_FILE, "w") as file:
        json.dump(USER_DATABASE, file)
    return { "message": f'The user {user} has been deleted' }
