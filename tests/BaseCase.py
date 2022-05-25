import unittest

from app import app
from db import db


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()
