from fastapi import FastAPI
from .routers import users, workouts, plans

app = FastAPI(title="Coach Live Platform")

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(plans.router)
