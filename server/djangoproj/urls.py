"""Top-level routes for the Cars Dealership application."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


SPA = TemplateView.as_view(template_name="Home.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("about", TemplateView.as_view(template_name="About.html")),
    path("contact", TemplateView.as_view(template_name="Contact.html")),
    path("", SPA),
    path("dealers", SPA),
    path("dealer/<int:dealer_id>", SPA),
    path("postreview/<int:dealer_id>", SPA),
    path("login", SPA),
    path("register", SPA),
]
