from httpx import get
from discord_webhook import DiscordWebhook, DiscordEmbed

from config import WEBHOOK
from app.logger import log

def send_log(discord_id: int, discord_username: str, email: str, ip: str):
    webhook = DiscordWebhook(WEBHOOK)
    embed = DiscordEmbed(
        title="New user authenticated",
        description=(
            "`👤` **Identity**\n"
            f"```{discord_username} - {discord_id}```\n"
            "`📧` **Email**\n"
            f"```{email}```\n"
            "`🛰️` **IP**\n"
            f"```{ip}```"
        ),
        color=0x2b2d31
    )
    webhook.add_embed(embed)
    result = webhook.execute()

    if result.status_code != 200:
        return log.error(f"{ip} ({discord_username}) - Could not send webhook log. Response: {result.json()}")
    
def get_user_data(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    result = get("https://discord.com/api/users/@me", headers=headers)
    return result