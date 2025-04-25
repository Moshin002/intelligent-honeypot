from flask import app
from app.auth import auth


@app.route('/secure')
@auth.login_required
def secure():
    return "This is a protected area!"


@app.route('/wp-admin')
def fake_wpadmin():
    return "WordPress login", 200  # Bots will love this!


@app.route('/.env')
def fake_env():
    return "SECRET_KEY=attacker_will_steal_this", 200
