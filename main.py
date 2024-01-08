import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

GENDER = "male"
WEIGHT_KG = 72
HEIGHT_CM = 173
AGE = 24

today = datetime.now().strftime("%d/%m/%Y")
today_time = datetime.now().strftime("%X")

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

nutritionix_header = {
    "x-app-id": os.getenv("APP_ID"),
    "x-app-key": os.getenv("APP_KEY"),
}
sheety_header = {
    "Authorization": os.getenv("AUTHORIZATION"),
}
nutritionix_params = {
    "query": input("Tell me which exercises you did? "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

nutritionix_response = requests.post(
    url=nutritionix_endpoint,
    headers=nutritionix_header,
    json=nutritionix_params,
)
nutritionix_nlp = nutritionix_response.json()
for exercise in nutritionix_nlp["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheety_response = requests.post(
        url=os.getenv("SHEETY_ENDPOINT"),
        json=sheet_inputs,
        headers=sheety_header,
        auth=(
            os.getenv("USERNAME"),
            os.getenv("PASSWORD"),
        )
    )
