from redbot.core import Config, commands, checks
from redbot.cogs.admin import admin
import asyncio
import aiohttp
import discord
import time

class wprune(commands.Cog):
    """Wysc Prune Management"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=822775204043948063)
        default_guild = {
            "placeholder": "placeholder"
        }

        self.config.register_guild(**default_guild)

    async def red_get_data_for_user(self, *, user_id: int):
        return "This cog stores your public Discord User ID for the purposes of maintaining the Wysc service."

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not story any data
        pass


    # Utility Commands

    def getRoleMembers(self, ctx, role: discord.Role):
        a = role.members
        roleIdList = [b.id for b in a]
        return roleIdList

    def getListDifference(self, listone, listtwo):
        # Listone: Seeds, Listtwo: Sprouts
        return set(listone).difference(listtwo)

    # Bot Commands

    @commands.command()
    async def getrolemembers(self, ctx, role: discord.Role):
        """List Role One Members"""
        await ctx.send(self.getRoleMembers(ctx, role))

    @commands.command()
    async def roledifference(self, ctx, role1: discord.Role, role2: discord.Role):
        """List Differences in the two roles"""
        a = self.getRoleMembers(ctx, role1)
        b = self.getRoleMembers(ctx, role2)
        await ctx.send(self.getListDifference(a, b))

