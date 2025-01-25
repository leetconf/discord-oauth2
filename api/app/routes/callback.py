from httpx import post
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta, timezone

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from app import db
from app.logger import log
from app.models.user_model import User
from app.utils import send_log, get_user_data

callback_bp = Blueprint("callback", __name__)

@callback_bp.get("/callback")
def callback():
    code = request.args.get("code")
    ip = request.remote_addr

    if not code:
        return jsonify(success=False, message="No code provided"), 400

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': "identify email guilds.join",
    }

    response = post("https://discord.com/api/oauth2/token", headers=headers, data=data)
    json_response = response.json()
    
    if response.status_code != 200:

        if json_response["error"] == "invalid_grant":
            return jsonify(success=False, message="Invalid code"), 400

        log.error(f"{ip} - Failed to retrieve tokens. Status: {response.status_code}, Response: {json_response}")
        return jsonify(success=False, message="Failed to authenticate"), 500

    expires_in = json_response["expires_in"]
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    access_token = json_response["access_token"]
    refresh_token = json_response["refresh_token"]

    result = get_user_data(access_token)

    if result.status_code != 200:
        log.error(f"{ip} - Failed to fetch user profile. Response: {result.json()}")
        return jsonify(success=False, message="Failed to fetch profile"), 500

    profile = result.json()

    discord_id = profile["id"]
    discord_username = profile["username"]
    email = profile["email"]

    if User.query.filter_by(discord_username=discord_username).first():
        return jsonify(success=False, message="You have already verified"), 409
            
    new_user = User(
        discord_id=discord_id,
        discord_username=discord_username,
        email=email,
        ip=ip,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at
    )

    db.session.add(new_user)
    db.session.commit()

    send_log(discord_id, discord_username, email, ip)
    return jsonify(success=True, message="Successfully verified"), 200