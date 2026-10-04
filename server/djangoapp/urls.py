"""URL routes for dealership APIs and authentication."""

from django.urls import path

from . import views


app_name = "djangoapp"
urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.registration, name="register"),
    path("get_dealers", views.get_dealerships, name="dealers"),
    path("get_dealers/<str:state>", views.get_dealerships, name="dealers-state"),
    path("dealer/<int:dealer_id>", views.get_dealer_details, name="dealer"),
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="reviews"),
    path("add_review", views.add_review, name="add-review"),
    path("get_cars", views.get_cars, name="cars"),
]
