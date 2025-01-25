from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    discord_id = db.Column(db.Integer, nullable=False)
    discord_username = db.Column(db.String, nullable=False)

    email = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=False)
    
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "discord_id": self.discord_id,
            "discord_username": self.discord_username,
            "email": self.email,
            "ip": self.ip,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.isoformat()
        }
