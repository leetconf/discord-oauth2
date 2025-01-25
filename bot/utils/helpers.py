import requests
from config import BACKEND, BACKEND_SECRET, CLIENT_ID, CLIENT_SECRET, BOT_TOKEN
from .logger import log

def init_session():
    session = requests.Session()
    session.headers = {"X-Secret-Key": BACKEND_SECRET}
    return session

class Auth:
    def __init__(self, discord_id: int, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.discord_id = discord_id

    def refresh_tokens(self):
        url = "https://discord.com/api/oauth2/token"
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "redirect_uri": f"{BACKEND}/callback",
            "scope": "identify email guilds.join"
        }
        response = requests.post(url, data=data)
        response_data = response.json()

        if response.status_code != 200:
            return log.error(f"Could not refresh tokens ({self.refresh_token}). Response: {response.json()}")
        
        session = init_session()
        backend_response = session.patch(f"{BACKEND}/api/users/{self.discord_id}", json=response_data)

        if response.status_code != 200:
            return log.error(f"Could not update access/refresh tokens through backend. Status: {backend_response.status_code}")

        self.access_token = response_data["access_token"]
        self.refresh_token = response_data["refresh_token"]

    def add_to_guild(self, guild_id: int):
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{self.discord_id}"
        json = {"access_token": self.access_token}
        headers = {"Authorization": f"Bot {BOT_TOKEN}"}

        response = requests.put(url, headers=headers, json=json)
        json_response = response.json()

        if response.status_code == 403:
            session = init_session()
            backend_response = session.delete(f"{BACKEND}/api/users/{self.discord_id}")

            if backend_response.status_code != 200:
                log.error(f"Could not perform a user deletion operation through backend. Status: {backend_response.status_code}")
                
            return

        if response.status_code != 201:
            log.error(f"Could not add user to guild. Response: {json_response}. Status: {response.status_code}")