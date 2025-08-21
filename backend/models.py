from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Role(str, Enum):
    admin = "admin"
    coach = "coach"
    user = "user"


class UserBase(BaseModel):
    username: str
    role: Role


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pass


class Workout(BaseModel):
    user: str
    type: str
    distance_km: float
    duration_min: float


class PlanRequest(BaseModel):
    goal: str
    sport: str


class PlanResponse(BaseModel):
    message: str
    workouts: List[str]


class NutritionRequest(BaseModel):
    calories: int
    diet: Optional[str] = None


class NutritionPlan(BaseModel):
    message: str
    meals: List[str]
