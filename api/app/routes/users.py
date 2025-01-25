from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta, timezone

from app import db
from app.models.user_model import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.get("/")
def get_users():
    users = User.query.all()
    json_users = [user.to_dict() for user in users]
    return jsonify(success=True, data=json_users), 200

@users_bp.patch("/<id>")
def edit_user(id):
    user = User.query.filter_by(discord_id=id).first()
    if not user: return jsonify(success=False, message="User not found"), 404
    
    data = request.get_json()

    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    expires_in = data.get("expires_in")

    if access_token:
        user.access_token = access_token

    if refresh_token:
        user.refresh_token = refresh_token

    if expires_in:
        user.expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))

    db.session.commit()
    return jsonify(success=True, message="User updated"), 200

@users_bp.delete("/<id>")
def remove_user(id):
    user = User.query.filter_by(discord_id=id).first()
    if not user: return jsonify(success=False, message="User not found"), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(success=True, message="User deleted"), 200