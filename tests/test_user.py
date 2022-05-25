import json
import unittest
from tests.BaseCase import BaseCase

name = "alex"
surname = "khantadze"
email = "alekoxanta@gmail.com"
password = "12345"


class RegistrationTest(BaseCase):
    def test_registration(self):
        payload = json.dumps({
            "name": name,
            "surname": surname,
            "email": email,
            "password": password
        })

        response = self.app.post("/register",
                                 headers={"Content-Type": "application/json"},
                                 data=payload)

        self.assertEqual(201, response.status_code)


class LoginTest(BaseCase):
    def test_login(self):
        payload = json.dumps({
            "name": name,
            "surname": surname,
            "email": email,
            "password": password
        })

        response = self.app.post("/register",
                                 headers={"Content-Type": "application/json"},
                                 data=payload)

        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post("/login",
                                 headers={"Content-Type": "application/json"},
                                 data=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual("alex", response.get_json()['user']['name'])
