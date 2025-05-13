from flask import Blueprint, render_template, redirect, url_for
from app.services.auth_service import AuthService

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/dashboard')
@AuthService.token_required
def dashboard(user):
    return render_template('dashboard.html', user=user)

@web.route('/download/<int:session_id>')
@AuthService.token_required
def download_config(user, session_id):
    # This would serve the config file for download
    return redirect(url_for('web.dashboard'))