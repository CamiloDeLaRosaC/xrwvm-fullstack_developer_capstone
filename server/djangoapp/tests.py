"""Integration tests for the dealership API."""

import json

from django.contrib.auth.models import User
from django.test import TestCase


class DealershipApiTests(TestCase):
    """Exercise authentication and public catalog endpoints."""

    def setUp(self):
        User.objects.create_user(username="demo", password="DemoPass123!")

    def test_login(self):
        response = self.client.post(
            "/djangoapp/login",
            json.dumps({"userName": "demo", "password": "DemoPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")

    def test_dealers_and_kansas_filter(self):
        self.assertGreater(len(self.client.get("/djangoapp/get_dealers").json()["dealers"]), 1)
        dealers = self.client.get("/djangoapp/get_dealers/Kansas").json()["dealers"]
        self.assertTrue(dealers)
        self.assertTrue(all(dealer["state"] == "Kansas" for dealer in dealers))

    def test_dealer_details_and_reviews(self):
        self.assertEqual(self.client.get("/djangoapp/dealer/8").json()["dealer"][0]["id"], 8)
        self.assertEqual(self.client.get("/djangoapp/reviews/dealer/15").status_code, 200)

    def test_car_catalog(self):
        response = self.client.get("/djangoapp/get_cars").json()
        self.assertTrue(response["CarMakes"])
        self.assertTrue(response["CarModels"])
