from app import db

class Server(db.Model):
    __tablename__ = 'servers'
    
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(120), unique=True, nullable=False)
    ip_address = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, default=100)
    current_connections = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    sessions = db.relationship('Session', backref='server', lazy=True)
    
    def __repr__(self):
        return f'<Server {self.hostname} ({self.location})>'