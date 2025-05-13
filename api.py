from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.services.vpn_service import VPNService
from app.models import Session, User

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = AuthService.generate_token(user)
    return jsonify({'token': token, 'is_premium': user.is_premium})

@api.route('/start', methods=['POST'])
@AuthService.token_required
def start_session(user):
    client_ip = request.remote_addr
    session = VPNService.start_session(user, client_ip)
    
    if not session:
        return jsonify({'message': 'No available servers'}), 503
        
    return jsonify({
        'config': session.client_config,
        'session_id': session.id,
        'duration': session.remaining_time(user)
    })

@api.route('/status/<int:session_id>', methods=['GET'])
@AuthService.token_required
def session_status(user, session_id):
    session = Session.query.get(session_id)
    if not session or session.user_id != user.id:
        return jsonify({'message': 'Session not found'}), 404
        
    return jsonify({
        'is_active': session.is_active,
        'remaining': session.remaining_time(user),
        'server_location': session.server.location
    })

@api.route('/end/<int:session_id>', methods=['POST'])
@AuthService.token_required
def end_session(user, session_id):
    session = Session.query.get(session_id)
    if not session or session.user_id != user.id:
        return jsonify({'message': 'Session not found'}), 404
        
    VPNService.end_session(session)
    return jsonify({'message': 'Session ended'})