"""Helpers for optional external dealership microservices."""

import os

import requests
from dotenv import load_dotenv


load_dotenv()
BACKEND_URL = os.getenv("backend_url", "http://localhost:3030")
SENTIMENT_URL = os.getenv("sentiment_analyzer_url", "http://localhost:5050")


def get_request(endpoint, **kwargs):
    """Perform a GET request against the dealership service."""
    response = requests.get(
        f"{BACKEND_URL}/{endpoint.lstrip('/')}",
        params=kwargs or None,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    """Return the sentiment produced by the analyzer service."""
    response = requests.get(f"{SENTIMENT_URL}/analyze/{text}", timeout=10)
    response.raise_for_status()
    return response.json().get("sentiment", "neutral")


def post_review(data_dict):
    """Submit a review to the dealership service."""
    response = requests.post(
        f"{BACKEND_URL}/insert_review",
        json=data_dict,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
