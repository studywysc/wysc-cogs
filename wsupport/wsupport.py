from redbot.core import Config, commands, checks
from redbot.cogs.admin import admin
from github import Github
import asyncio
import aiohttp
import discord
import time

class wsupport(commands.Cog):
    """Wysc Roles Management"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=822775204043948063)
        default_guild = {
            "placeholder": "placeholder"
        }

        self.config.register_guild(**default_guild)

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not story any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not story any data
        pass


    # Utility Commands

    def getGithubToken(self, ctx)
        gaccess = await self.bot.get_shared_api_tokens("github")
        if gaccess.get("api_key") is None:
            return None
        else:
            return gaccess.get("api_key")


    # Bot Commands

