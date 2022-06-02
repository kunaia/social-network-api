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


def logout(app, token, refresh=False):
    return app.post("/logout" + ("2" if refresh else ""),
                    headers={
                        "Content-Type": "application/json",
                        'Authorization': 'Bearer ' + token
                    })


class RegistrationTest(BaseCase):
    def test_successful_registration(self):
        response = register(self.app)
        self.assertEqual(201, response.status_code)

    def test_unsuccessful_registration(self):
        response = register(self.app, email="somenonvalidemail@notvalid.com")

        self.assertEqual(400, response.status_code)
        self.assertEqual(None, response.json.get("user", None))


class LoginTest(BaseCase):
    def test_successful_login(self):
        response = register(self.app, name="random_name")
        response = login(self.app)

        self.assertEqual(200, response.status_code)
        self.assertEqual("random_name", response.get_json()['user']['name'])

    def test_unsuccessful_login(self):
        response = login(self.app)
        self.assertEqual(404, response.status_code)


class LogoutTest(BaseCase):
    def test_Logout(self):
        response = register(self.app)
        response = login(self.app)
        access_token = response.json.get("access_token", None)
        refresh_token = response.json.get("refresh_token", None)

        response1 = logout(self.app, token=access_token)
        response2 = logout(self.app, token=refresh_token, refresh=True)

        self.assertEqual(200, response1.status_code)
        self.assertEqual(200, response2.status_code)


class UserInfoTest(BaseCase):
    def test_user_info(self):
        response = register(self.app, name="someone")
        response = login(self.app)
        response = self.app.get(
            "/user",
            headers={
                "Content-Type": "application/json",
                'Authorization': 'Bearer ' + response.json["access_token"]
            }
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("someone", response.json["user"]["name"])
