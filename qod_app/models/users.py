# -*- coding: UTF-8 -*-

"""
users.py

Model declaration for User used in database
"""

from passlib.apps import custom_app_context as pwd_context

from ..extensions import db


class User(db.Model):
    """User model"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    role = db.Column(db.String(32), default='invite')
    password_hash = db.Column(db.String(128))

    # methods object to do secure password verification
    # Cf. https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
    def hash_password(self, password: str) -> None:
        """Hash the password (based on sha256_crypt hashing algorithm [passlib]) before
        store the hash in the database, this to avoid storing it in plain text.

        :param password: plain text password
        :type: str
        :return: None
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password: str) -> bool:
        """Compare the password hash to the plain password to
        check if it is correct or not

        :param password: plain text password
        :type: str
        :return: True if the password is correct else False
        """
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def add_user(user):
        """A simple Object method to store a new user to
        the database (don't forget to hash the password before)

        :param user:
        :return:
        """
        db.session.add(user)
        db.session.commit()
