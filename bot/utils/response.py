from discord import Interaction, Embed
from config import FAILURE_EMOJI, SUCCESS_EMOJI

class Response:
    def __init__(self, interaction: Interaction, message: str, custom_emoji: str = None, ephemeral: bool = False) -> None:
        self.ephemeral = ephemeral
        self.message = message
        self.custom_emoji = custom_emoji
        self.interaction = interaction
        
    async def success(self) -> None:
        embed = Embed(
            description=f"{SUCCESS_EMOJI} {self.interaction.user.mention}: {self.message}",
            color=0xA5EB78
        )
        await self.interaction.response.send_message(embed=embed, ephemeral=self.ephemeral)
        
    async def failure(self) -> None:
        embed = Embed(
            description=f"{FAILURE_EMOJI} {self.interaction.user.mention}: {self.message}",
            color=0xFFD43A
        )
        await self.interaction.response.send_message(embed=embed, ephemeral=self.ephemeral)