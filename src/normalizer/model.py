from sqlalchemy.exc import IntegrityError

from init import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(
        db.String(1000)
    )
    last_name = db.Column(
        db.String(1000)
    )
    gender = db.Column(
        db.String(10)
    )
    email = db.Column(
        db.String(1000)
    )
    country = db.Column(
        db.String(10)
    )
    date_of_birth = db.Column(db.DateTime())

    @staticmethod
    def set_users(users):
        for user in users:
            user = User(**user)
            db.session.add(user)
        try:
            db.session.commit()
            return {'id': user.id}
        except IntegrityError as ex:
            return {'error': str(ex.orig)}
