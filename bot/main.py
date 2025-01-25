import asyncio

from discord import app_commands, Intents, Interaction
from discord.ext import commands

from config import BOT_TOKEN, COGS
from utils.logger import log
from utils.response import Response

intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.tree.error
async def on_app_command_error(interaction: Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await Response(interaction, "You don't have the **permitted role** to use this command").failure()

    elif isinstance(error, app_commands.MissingPermissions):
        await Response(interaction, "You **lack** permission(s) to use this command").failure()

    elif isinstance(error, app_commands.errors.CommandInvokeError):
        await Response(interaction, "Something went wrong").failure()
        log.critical(error.original)

async def load_cogs() -> None:
    for cog in COGS:
        try:
            await bot.load_extension(cog)
        except Exception as e:
            log.error(f"Error loading {cog}: {e}")

async def main():
    async with bot:
        await load_cogs()
        try:
            await bot.start(BOT_TOKEN)
        except Exception as e:
            log.error(f"Error on login: {e}")

if __name__ == "__main__":
    asyncio.run(main())