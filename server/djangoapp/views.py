# Uncomment the required imports before adding the code

from datetime import datetime  # noqa: F401 (保留如需时间戳)
import json
import logging

from django.contrib import messages  # noqa: F401 (保留如需消息)
from django.contrib.auth import authenticate, login, logout as dj_logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render  # noqa: F401
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """Handle sign-in."""
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("userName", "")
    password = data.get("password", "")

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}, status=200
        )
    return JsonResponse({"userName": username, "status": "Unauthorized"}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def logout_request(request):
    """Handle sign-out (避免与 django.contrib.auth.logout 名称冲突)."""
    dj_logout(request)
    return JsonResponse({"userName": ""}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    """Handle sign-up."""
    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("userName", "")
    password = data.get("password", "")
    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")
    email = data.get("email", "")

    if not username or not password:
        return JsonResponse({"error": "Missing fields"}, status=400)

    try:
        User.objects.get(username=username)
        # 已存在
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}, status=409
        )
    except User.DoesNotExist:
        logger.debug("%s is new user", username)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"}, status=201)


def get_dealerships(request, state="All"):
    """Return dealerships list, optionally filtered by state."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint) or []
    return JsonResponse({"status": 200, "dealers": dealerships}, status=200)


def get_dealer_details(request, dealer_id):
    """Return a single dealer details."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint) or {}
    return JsonResponse({"status": 200, "dealer": dealership}, status=200)


def get_dealer_reviews(request, dealer_id):
    """Return reviews for a dealer, with sentiment analysis (安全兜底)."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint) or []

    safe_reviews = []
    for item in reviews:
        # 兼容后端字段缺失
        review_text = (item or {}).get("review", "")
        sentiment_resp = analyze_review_sentiments(review_text) or {}
        sentiment = sentiment_resp.get("sentiment", "neutral")

        # 合并原数据并补齐 sentiment
        merged = dict(item or {})
        merged["sentiment"] = sentiment
        safe_reviews.append(merged)

    return JsonResponse({"status": 200, "reviews": safe_reviews}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    """Submit a review; require authenticated user."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"}, status=403)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": 400, "message": "Invalid JSON"}, status=400)

    resp = post_review(data)
    if resp is None:
        return JsonResponse(
            {"status": 502, "message": "Error in posting review"}, status=502
        )
    return JsonResponse({"status": 200, "result": resp}, status=200)


def get_cars(request):
    """Lazy-init demo data, then return (CarModel, CarMake) pairs."""
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars}, status=200)
