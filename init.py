# app/services/__init__.py

from .auth_service import AuthService
from .vpn_service import VPNService

# Initialize service instances
auth_service = AuthService()
vpn_service = VPNService()

# Export services for easy access
__all__ = ['auth_service', 'vpn_service']