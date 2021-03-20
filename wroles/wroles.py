from redbot.core import Config, commands, checks
from redbot.cogs.admin import admin
import asyncio
import aiohttp
import discord
import time

class wroles(commands.Cog):
    """Wysc Roles Management"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=822775204043948063)
        default_guild = {
            "approvedroles": [],
            "rolemsgs": []
        }

        """ template
        "approvedroles": [ role_id, role_id, ... ],
        "rolemsgs": [
            {
                "name": "name",
                "title": "top of the embed",
                "body": "body content here",
                "roles": [
                    [emoji, role_id],
                    [emoji, role_id]
                ]
            }
        ]
        """

        self.config.register_guild(**default_guild)

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not story any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not story any data
        pass


    # @commands.has_role("Tree")
    
    @commands.guild_only()
    @commands.group()
    async def treeroles(self, ctx: commands.Context):
        """Role management for Trees"""
        if not ctx.invoked_subcommand:
            pass

    @treeroles.command(name="create")
    async def treerolescreate(self, ctx, roleName, hexColor=""):
        """Create a pingable role (for Cafe Events and #hangouts)
        
        Please make sure your event shows demonstrated interest first!
        Demonstrated interest can be pre-planned meetups of 5+ users, or at least 3 consecutive events, or some form of community benefit to having a pingable role.
        
        For a role name with spaces, wrap them in quotation marks ("Among Us")
        """
        if hexColor == "":
            role = await ctx.guild.create_role(name=roleName, mentionable=True)
        else:
            role = await ctx.guild.create_role(name=roleName, mentionable=True, colour = discord.Colour(int(f"0x{hexColor}", 16)))

        await ctx.author.add_roles(role)
        await ctx.send(f"{role.mention} is created and ready for use!")

    @treeroles.command(name="edit")
    async def treerolesedit(self, ctx, roleName, hexColor=""):
        """Create a pingable role (for Cafe Events and #hangouts)
        
        Please make sure your event shows demonstrated interest first!
        Demonstrated interest can be pre-planned meetups of 5+ users, or at least 3 consecutive events, or some form of community benefit to having a pingable role.
        
        For a role name with spaces, wrap them in quotation marks ("Among Us")
        """
        if hexColor == "":
            role = await ctx.guild.create_role(name=roleName, mentionable=True)
        else:
            role = await ctx.guild.create_role(name=roleName, mentionable=True, colour = discord.Colour(int(f"0x{hexColor}", 16)))

        await ctx.author.add_roles(role)
        await ctx.send(f"{role.mention} is created and ready for use!")

    # Future: Add a walkthrough command that asks for responses from user and does stuff based on response
