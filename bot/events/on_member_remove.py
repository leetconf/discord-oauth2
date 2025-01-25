from discord.ext import commands
from discord import Member
from datetime import datetime, timezone

from utils.helpers import init_session, Auth
from utils.logger import log
from config import BACKEND

class onMemberRemove(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        session = init_session()
        response = session.get(f"{BACKEND}/api/users")

        if response.status_code != 200:
            return log.error(f"Could not fetch users from backend. Status: {response.status_code}")
        else:
            users = response.json()["data"]
    
        user = next((user for user in users if user["discord_id"] == member.id), None)
        if not user: return
        
        auth = Auth(user["discord_id"], user["access_token"], user["refresh_token"])
        expiration_datetime = datetime.fromisoformat(user["expires_at"]).replace(tzinfo=timezone.utc)

        if datetime.now(timezone.utc) > expiration_datetime:
            auth.refresh_tokens()

        auth.add_to_guild(member.guild.id)

async def setup(bot):
    await bot.add_cog(onMemberRemove(bot))