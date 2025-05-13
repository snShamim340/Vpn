import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from app.models import User
from app.config import Config

class AuthService:
    @staticmethod
    def generate_token(user):
        """Generate JWT token for user"""
        token = jwt.encode({
            'sub': user.id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXPIRATION)
        }, Config.SECRET_KEY, algorithm='HS256')
        
        return token

    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return User.query.get(payload['sub'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def token_required(f):
        """Decorator for token-protected routes"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                return jsonify({'message': 'Token is missing!'}), 401
                
            token = token.split(' ')[1]
            user = AuthService.verify_token(token)
            if not user:
                return jsonify({'message': 'Token is invalid!'}), 401
                
            return f(user, *args, **kwargs)
        return decorateddecorated