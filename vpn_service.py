import os
import random
import subprocess
from app.models import Server, Session
from app import db

class VPNService:
    @staticmethod
    def get_available_server():
        """Get server with lowest load"""
        return Server.query.filter_by(is_active=True)\
                          .order_by(Server.current_connections)\
                          .first()

    @staticmethod
    def generate_client_config(user, server):
        """Generate OpenVPN/WireGuard config for client"""
        # This would be replaced with actual config generation logic
        config = f"""
        # Veil VPN Configuration for {user.username}
        # Server: {server.hostname} ({server.location})
        # {'PREMIUM ACCOUNT' if user.is_premium else 'FREE ACCOUNT - ADS ENABLED'}
        
        [Interface]
        PrivateKey = {{client_private_key}}
        Address = {{assigned_ip}}
        DNS = 1.1.1.1, 1.0.0.1
        
        [Peer]
        PublicKey = {{server_public_key}}
        Endpoint = {server.ip_address}:51820
        AllowedIPs = 0.0.0.0/0
        """
        
        return config.strip()

    @staticmethod
    def start_session(user, client_ip):
        """Start a new VPN session"""
        server = VPNService.get_available_server()
        if not server:
            return None
            
        config = VPNService.generate_client_config(user, server)
        
        session = Session(
            user_id=user.id,
            server_id=server.id,
            client_ip=client_ip,
            client_config=config,
            is_active=True
        )
        
        server.current_connections += 1
        db.session.add(session)
        db.session.commit()
        
        # Here you would actually setup the VPN on the server
        # subprocess.run([...])
        
        return session

    @staticmethod
    def end_session(session):
        """End an active VPN session"""
        session.is_active = False
        session.end_time = db.func.current_timestamp()
        
        server = session.server
        server.current_connections -= 1
        
        db.session.commit()
        
        # Here you would actually teardown the VPN on the server
        # subprocess.run([...])
        
        return TrueTrue