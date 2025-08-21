from fastapi import Header, HTTPException, status, Depends
from .database import users
from .models import Role, User


def get_current_user(x_user: str = Header(...), x_role: str = Header(...)) -> User:
    user = users.get(x_user)
    if not user or user.role != x_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


def require_role(required: Role):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return user
    return role_checker
