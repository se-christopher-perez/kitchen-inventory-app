from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=True)
    _password_hash = db.Column(db.String, nullable=False)

    @property
    def password_hash(self):
        raise AttributeError("password_hash is not readable")
    
    @password_hash.setter
    def password_hash(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    @validates('username')
    def validate_username(self, key, value):
        if not value or len(value) < 8:
            raise ValueError('Username must be at least 8 characters')
        return value