from typing import Dict, List
from .models import User, Workout

# In-memory storage. Replace with a real database in production.
users: Dict[str, User] = {}
workouts: Dict[str, List[Workout]] = {}
