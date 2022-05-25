from db import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError


class BaseModel:
    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def remove_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except (ValueError, StaleDataError):
            db.session.rollback()
            return False
