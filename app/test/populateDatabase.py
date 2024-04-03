from datetime import datetime
import pandas as pd
import os
import csv
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

def get_token(username, password):
    endpoint = f"{BASE_URL}/token"
    data = {"username": username, "password": password}
    response = requests.post(endpoint, data=data)
    return response.json().get("access_token")

def create_user(token, username, email, password):
    endpoint = f"{BASE_URL}/users/"
    headers = {"Authorization": f"Bearer {token}"}
    user_data = {"username": username, "email": email, "password": password, "role": "USER"}
    response = requests.post(endpoint, json=user_data, headers=headers)
    return response.json()

def upload_ecg(token, ecg):
    endpoint = f"{BASE_URL}/ecgs/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(endpoint, json=ecg, headers=headers)
    return response.json()

def get_ecg_insight(token, ecg_id):
    endpoint = f"{BASE_URL}/ecgs/{ecg_id}/insights/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

admin_token = get_token(ADMIN_USERNAME, ADMIN_PASSWORD)
print("Admin token:", admin_token)

user_data = {"username": "test_user", "email": "test@example.com", "password": "password123"}
create_user(admin_token, **user_data)
print("User created.")

user_token = get_token(user_data["username"], user_data["password"])
print("User token:", user_token)

module_dir = os.path.dirname(os.path.abspath(__file__))
files_path = os.path.join(module_dir, "files")
lead_names = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]

for filename in os.listdir(files_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(files_path, filename)
        leads = []
        with open(file_path, "r", newline="") as file:
            df = pd.read_csv(file_path, header=None, names=lead_names)
        df = df.astype(int)
        for idx, lead_name in enumerate(lead_names):
            leads.append({"name": lead_name, "samples": 5000, "signal": list(df.iloc[:, idx])})
        ecg = {"date": "2024-04-02T23:50:37.231Z", "leads": leads}
        upload_ecg(user_token, ecg)

insights = get_ecg_insight(user_token, 1)
print("insights for ecg 1", insights)
