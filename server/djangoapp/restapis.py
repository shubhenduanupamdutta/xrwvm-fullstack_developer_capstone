import os
from typing import Any

import requests
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("BACKEND_URL", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "SENTIMENT_ANALYZER_URL",
    default="http://localhost:5050/",
)


def get_request(endpoint: str, **kwargs: str) -> JsonResponse | None:
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print(f"GET from {request_url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url, timeout=90)
        return response.json()
    except:  # noqa: E722
        # If any error occurs
        print("Network exception occurred")


def analyze_review_sentiments(text: str) -> JsonResponse | None:
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url, timeout=90)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict: dict[str, Any]) -> JsonResponse | None:
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=90)
        print(response.json())
        return response.json()
    except:  # noqa: E722
        print("Network exception occurred")
