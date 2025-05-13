import time
from datetime import datetime
from app import create_app
from app.models import Session, User
from app.services.vpn_service import VPNService

app = create_app()

def check_sessions():
    with app.app_context():
        active_sessions = Session.query.filter_by(is_active=True).all()
        
        for session in active_sessions:
            user = session.user
            remaining = session.remaining_time(user)
            
            if remaining <= 0:
                print(f"Ending session {session.id} for user {user.username}")
                VPNService.end_session(session)
            elif remaining < 300:  # 5 minutes remaining
                print(f"Warning: Session {session.id} has {remaining//60} minutes remaining")

if __name__ == '__main__':
    while True:
        check_sessions()
        time.sleep(60)  # Check every minuteminute