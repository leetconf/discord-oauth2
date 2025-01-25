from discord import app_commands, Interaction
from discord.ext import commands
from utils.response import Response
from config import CLIENT_ID, WHITELIST_ROLE, BACKEND
from urllib.parse import urlencode

class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_message = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="oauth2", description="Generates oAuth2 URL")
    @app_commands.checks.has_role(WHITELIST_ROLE)
    async def oauth2(self, interaction: Interaction):
        scopes = ["email", "guilds.join", "identify"]
        base_url = "https://discord.com/oauth2/authorize"
        query_params = {
            "client_id": CLIENT_ID,
            "redirect_uri": f"{BACKEND}/callback",
            "response_type": "code",
            "scope": " ".join(scopes)
        }
        oauth2_url = f"{base_url}?{urlencode(query_params)}"
        await Response(interaction, f"[Here ya go]({oauth2_url})").success()

async def setup(bot):
    await bot.add_cog(Link(bot))