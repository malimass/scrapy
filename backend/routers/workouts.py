from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .. import models, database, auth

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/", response_model=models.Workout)
def add_workout(workout: models.Workout, current=Depends(auth.get_current_user)):
    if workout.user != current.username:
        raise HTTPException(status_code=400, detail="Workout user mismatch")
    database.workouts.setdefault(current.username, []).append(workout)
    return workout


@router.get("/", response_model=List[models.Workout])
def list_workouts(current=Depends(auth.get_current_user)):
    return database.workouts.get(current.username, [])
