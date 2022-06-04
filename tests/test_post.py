import json
import random

from tests.BaseCase import BaseCase
from tests.test_user import login, register


def create_post(app, body=None, access_token=None):
    payload = json.dumps({
        "body": body if body is not None else "some random text"
    })
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"
    response = app.post("/post",
                        headers=headers,
                        data=payload)
    return response


def get_post(app, post_id, access_token=None):
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"
    response = app.get(f"/post/{post_id}",
                       headers=headers)
    return response


def update_post(app, post_id, new_body, access_token=None):
    payload = json.dumps({"body": new_body})
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"
    response = app.put(f"/post/{post_id}",
                       headers=headers,
                       data=payload)
    return response


def delete_post(app, post_id, access_token=None):
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers['Authorization'] = f"Bearer {access_token}"
    response = app.delete(f"/post/{post_id}",
                          headers=headers)
    return response


class PostCrudTests(BaseCase):
    def test_post_crud(self):
        register_response = register(app=self.app)
        login_response = login(app=self.app)

        my_text = f"my test text {random.randint(1, 10 ** 6)}"
        response = create_post(app=self.app,
                               body=my_text,
                               access_token=login_response.json['access_token'])

        # create
        self.assertEqual(response.status_code, 201, msg="error in creating process")

        response = get_post(app=self.app, post_id=response.json['post']["id"],
                            access_token=login_response.json['access_token'])

        # read
        self.assertEqual(my_text, response.json["post"]["body"])

        my_new_next = f"my random text {random.randint(1, 10 ** 6)}"
        post_id = response.json['post']["id"]
        response = update_post(self.app, post_id=post_id, new_body=my_new_next,
                               access_token=login_response.json['access_token'])
        response = get_post(app=self.app, post_id=post_id)

        # update
        self.assertEqual(my_new_next, response.json["post"]["body"])

        response1 = delete_post(app=self.app, post_id=post_id,
                                access_token=login_response.json['access_token'])
        response2 = get_post(app=self.app, post_id=post_id)

        # delete
        self.assertEqual(200, response1.status_code)
        self.assertEqual(404, response2.status_code)
