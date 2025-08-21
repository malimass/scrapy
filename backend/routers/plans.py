from fastapi import APIRouter, Depends
from .. import models, auth

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/training", response_model=models.PlanResponse)
def generate_plan(req: models.PlanRequest, current=Depends(auth.get_current_user)):
    workouts = [f"{req.sport} session {i+1} towards {req.goal}" for i in range(3)]
    return models.PlanResponse(message="Generated plan", workouts=workouts)


@router.post("/nutrition", response_model=models.NutritionPlan)
def nutrition(req: models.NutritionRequest, current=Depends(auth.get_current_user)):
    meals = [f"Meal {i+1} for {req.calories} calories" for i in range(3)]
    return models.NutritionPlan(message="Nutrition plan", meals=meals)
