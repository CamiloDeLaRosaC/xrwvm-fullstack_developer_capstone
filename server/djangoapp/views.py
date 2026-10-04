"""HTTP views for the Cars Dealership capstone application."""

import json
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel


DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "database" / "data"
RUNTIME_REVIEWS = Path(__file__).resolve().parent.parent / "runtime_reviews.json"


def _read_json(filename, key):
    with (DATA_DIRECTORY / filename).open(encoding="utf-8") as data_file:
        return json.load(data_file)[key]


def _reviews():
    reviews = _read_json("reviews.json", "reviews")
    if RUNTIME_REVIEWS.exists():
        with RUNTIME_REVIEWS.open(encoding="utf-8") as review_file:
            reviews.extend(json.load(review_file))
    return reviews


def _sentiment(text):
    lowered = text.lower()
    positive = ("fantastic", "excellent", "great", "good", "love", "helpful")
    negative = ("bad", "awful", "terrible", "poor", "hate", "worst")
    if any(word in lowered for word in positive):
        return "positive"
    if any(word in lowered for word in negative):
        return "negative"
    return "neutral"


def _body(request):
    return json.loads(request.body or "{}")


@csrf_exempt
def login_user(request):
    """Authenticate a user and establish a Django session."""
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    data = _body(request)
    username = data.get("userName") or data.get("username", "")
    user = authenticate(username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": username, "status": "Failed"}, status=401)
    login(request, user)
    return JsonResponse(
        {
            "userName": username,
            "status": "Authenticated",
            "firstName": user.first_name,
            "lastName": user.last_name,
        }
    )


def logout_user(request):
    """End the current authenticated session."""
    username = request.user.username if request.user.is_authenticated else "anonymous"
    logout(request)
    return JsonResponse({"userName": username, "status": "Logged out"})


@csrf_exempt
def registration(request):
    """Create and sign in a new application user."""
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    data = _body(request)
    username = data.get("userName") or data.get("username", "")
    if not username or User.objects.filter(username=username).exists():
        return JsonResponse(
            {"status": "Failed", "message": "Username is unavailable"},
            status=400,
        )
    user = User.objects.create_user(
        username=username,
        password=data.get("password"),
        email=data.get("email", ""),
        first_name=data.get("firstName", ""),
        last_name=data.get("lastName", ""),
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state=None):
    """Return every dealership, optionally filtered by state name or code."""
    dealers = _read_json("dealerships.json", "dealerships")
    requested_state = state or request.GET.get("state")
    if requested_state and requested_state.lower() not in ("all", "all states"):
        requested_state = requested_state.lower()
        dealers = [
            dealer
            for dealer in dealers
            if dealer["state"].lower() == requested_state
            or dealer["st"].lower() == requested_state
        ]
    return JsonResponse({"status": 200, "dealers": dealers})


def get_dealer_details(request, dealer_id):
    """Return one dealership by numeric identifier."""
    dealers = _read_json("dealerships.json", "dealerships")
    dealer = [item for item in dealers if item["id"] == dealer_id]
    return JsonResponse({"status": 200 if dealer else 404, "dealer": dealer})


def get_dealer_reviews(request, dealer_id):
    """Return reviews for a dealer with a computed sentiment label."""
    reviews = [review for review in _reviews() if review["dealership"] == dealer_id]
    for review in reviews:
        review["sentiment"] = _sentiment(review.get("review", ""))
    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    """Persist a submitted dealer review."""
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    data = _body(request)
    current_reviews = _reviews()
    data["id"] = max((review["id"] for review in current_reviews), default=0) + 1
    data["dealership"] = int(data["dealership"])
    data["car_year"] = int(data["car_year"])
    data["sentiment"] = _sentiment(data.get("review", ""))
    runtime = []
    if RUNTIME_REVIEWS.exists():
        with RUNTIME_REVIEWS.open(encoding="utf-8") as review_file:
            runtime = json.load(review_file)
    runtime.append(data)
    with RUNTIME_REVIEWS.open("w", encoding="utf-8") as review_file:
        json.dump(runtime, review_file, indent=2)
    return JsonResponse({"status": 200, "review": data})


def get_cars(request):
    """Return car makes and models from SQLite or bundled inventory data."""
    database_models = CarModel.objects.select_related("car_make").all()
    if database_models.exists():
        models = [
            {
                "CarMake": model.car_make.name,
                "CarModel": model.name,
                "CarType": model.car_type,
                "CarYear": model.year,
            }
            for model in database_models
        ]
    else:
        cars = _read_json("car_records.json", "cars")
        models = [
            {
                "CarMake": car["make"],
                "CarModel": car["model"],
                "CarType": car["bodyType"],
                "CarYear": car["year"],
            }
            for car in cars
        ]
    makes = sorted({model["CarMake"] for model in models})
    return JsonResponse({"CarMakes": makes, "CarModels": models})
