import json
import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request: HttpRequest) -> JsonResponse:
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request: HttpRequest) -> JsonResponse:
    # Get the user object based on session id in request
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)


@csrf_exempt
def registration(request: HttpRequest) -> HttpResponse:
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:  # noqa: E722
        # If not, simply log this is a new user
        logger.debug("%s is a new user.", username)
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    data = {"userName": username, "error": "Already Registered"}
    return JsonResponse(data)


def get_cars(request: HttpRequest) -> JsonResponse:
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships all by default, particular state if
# state is passed
def get_dealerships(request: HttpRequest, state: str = "All") -> JsonResponse:
    endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request: HttpRequest, dealer_id: str) -> JsonResponse:
    # if dealer id has been provided
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews: list[dict[str, str]] = get_request(endpoint)  # pyright: ignore[reportAssignmentType]
        for review_detail in reviews:
            response: dict[str, str] = analyze_review_sentiments(review_detail["review"])  # pyright: ignore[reportAssignmentType]
            print(response)
            review_detail["sentiment"] = response["sentiment"]
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request: HttpRequest, dealer_id: str) -> JsonResponse:
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request: HttpRequest) -> JsonResponse:
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        response = post_review(data)
        if response and response.get("status") == 200:  # noqa: PLR2004
            return JsonResponse({"status": 200})
        return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})
