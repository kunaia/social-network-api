import json
from datetime import datetime
from libs.abstractapi import get_holiday

from tests.BaseCase import BaseCase


def register(app,
             name="name", surname="surname",
             email="alekoxanta@gmail.com", password="12345"):
    payload = json.dumps({
        "name": name,
        "surname": surname,
        "email": email,
        "password": password
    })
    response = app.post("/register",
                        headers={"Content-Type": "application/json"},
                        data=payload)
    return response


def login(app, email='alekoxanta@gmail.com', password="12345"):
    payload = json.dumps({
        "email": email,
        "password": password
    })
    response = app.post("/login",
                        headers={"Content-Type": "application/json"},
                        data=payload)
    return response


class RegistrationTest(BaseCase):
    def test_successful_registration(self):
        response = register(self.app)
        self.assertEqual(201, response.status_code)

    def test_unsuccessful_registration(self):
        response = register(self.app, email="somenonvalidemail@notvalid.com")

        self.assertEqual(400, response.status_code)
        self.assertEqual(None, response.json.get("user", None))


class LoginTest(BaseCase):
    def test_login(self):
        response = register(self.app, name="random_name")
        response = login(self.app)

        self.assertEqual(200, response.status_code)
        self.assertEqual("random_name", response.get_json()['user']['name'])
