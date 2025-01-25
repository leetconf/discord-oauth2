from discord.ext import commands
from utils.logger import log
from discord import Status

class onReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=Status.idle)
        log.info(f"Logged in as: {self.bot.user}")

async def setup(bot):
    await bot.add_cog(onReady(bot))