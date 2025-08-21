from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .. import models, database, auth

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=models.User)
def create_user(user: models.UserCreate):
    if user.username in database.users:
        raise HTTPException(status_code=400, detail="Username exists")
    database.users[user.username] = models.User(username=user.username, role=user.role)
    return database.users[user.username]


@router.get("/", response_model=List[models.User])
def list_users(current=Depends(auth.require_role(models.Role.admin))):
    return list(database.users.values())


@router.get("/me", response_model=models.User)
def read_me(current=Depends(auth.get_current_user)):
    return current
