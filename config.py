import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///veil.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # VPN Configuration
    VPN_CONFIG_DIR = os.getenv('VPN_CONFIG_DIR', '/etc/veil/vpn')
    VPN_SERVER_IPS = os.getenv('VPN_SERVER_IPS', '').split(',')
    
    # Authentication
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 3600))  # 1 hour
    
    # Session Management
    FREE_SESSION_LIMIT = int(os.getenv('FREE_SESSION_LIMIT', 1800))  # 30 minutes
    PREMIUM_SESSION_LIMIT = int(os.getenv('PREMIUM_SESSION_LIMIT', 86400))  # 24 hours
    
    # Ad Configuration
    AD_SERVING_INTERVAL = int(os.getenv('AD_SERVING_INTERVAL', 300))  # 5 minutesminutes