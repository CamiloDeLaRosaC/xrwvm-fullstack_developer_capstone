"""Top-level routes for the Cars Dealership application."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from djangoapp import views


SPA = TemplateView.as_view(template_name="Home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("fetchDealers", views.get_dealerships, name="fetch-dealers"),
    path("fetchDealers/<str:state>", views.get_dealerships, name="fetch-dealers-state"),
    path("fetchDealer/<int:dealer_id>", views.get_dealer_details, name="fetch-dealer"),
    path(
        "fetchReviews/dealer/<int:dealer_id>",
        views.get_dealer_reviews,
        name="fetch-reviews",
    ),
    path("about", TemplateView.as_view(template_name="About.html")),
    path("contact", TemplateView.as_view(template_name="Contact.html")),
    path("", SPA),
    path("dealers", SPA),
    path("dealer/<int:dealer_id>", SPA),
    path("postreview/<int:dealer_id>", SPA),
    path("login", SPA),
    path("register", SPA),
]
