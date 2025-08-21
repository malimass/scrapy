import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.title("Coach Live Demo")

st.sidebar.header("Credentials")
username = st.sidebar.text_input("Username")
role = st.sidebar.selectbox("Role", ["user", "coach", "admin"])
headers = {"X-User": username, "X-Role": role}

st.header("Register User")
if st.button("Register"):
    res = requests.post(f"{API_URL}/users/", json={"username": username, "password": "x", "role": role})
    st.write(res.json())

st.header("My Workouts")
if st.button("Load Workouts"):
    res = requests.get(f"{API_URL}/workouts/", headers=headers)
    st.write(res.json())

st.subheader("Add Workout")
w_type = st.text_input("Type", "run")
distance = st.number_input("Distance (km)", value=5.0)
duration = st.number_input("Duration (min)", value=30.0)
if st.button("Save Workout"):
    payload = {"user": username, "type": w_type, "distance_km": distance, "duration_min": duration}
    res = requests.post(f"{API_URL}/workouts/", json=payload, headers=headers)
    st.write(res.json())

st.header("Training Plan")
goal = st.text_input("Goal", "10k")
sport = st.text_input("Sport", "run")
if st.button("Generate Plan"):
    res = requests.post(f"{API_URL}/plans/training", json={"goal": goal, "sport": sport}, headers=headers)
    st.write(res.json())

st.header("Nutrition Plan")
cal = st.number_input("Calories", value=2000)
diet = st.text_input("Diet preference", "")
if st.button("Generate Nutrition Plan"):
    payload = {"calories": cal}
    if diet:
        payload["diet"] = diet
    res = requests.post(f"{API_URL}/plans/nutrition", json=payload, headers=headers)
    st.write(res.json())
