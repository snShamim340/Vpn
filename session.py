from app import db
from datetime import datetime, timedelta

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    client_ip = db.Column(db.String(15))
    client_config = db.Column(db.Text)  # Stores the generated VPN config
    
    def remaining_time(self, user):
        """Calculate remaining session time based on user type"""
        if user.is_premium:
            limit = Config.PREMIUM_SESSION_LIMIT
        else:
            limit = Config.FREE_SESSION_LIMIT
            
        elapsed = datetime.utcnow() - self.start_time
        remaining = limit - elapsed.total_seconds()
        return max(0, remaining)
    
    def __repr__(self):
        return f'<Session {self.id} for User {self.user_id}>'