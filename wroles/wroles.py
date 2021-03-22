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
            "roleList": [],
            "roleMsgs": []
        }

        """ template
        "rolelist": [ role_id, role_id, ... ],
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


    # Utility Commands

    async def addToRoleList(self, ctx, roleName: discord.Role):
        """Add a role to the list of roles"""
        currentRoles = await self.config.guild(ctx.guild).roleList()
        currentRoles.append(roleName)
        await self.config.guild(ctx.guild).roleList.set(currentRoles)
        return True

    async def removeFromRoleList(self, ctx, roleName: discord.Role):
        """Remove a role from the list of roles"""
        currentRoles = await self.config.guild(ctx.guild).roleList()
        currentRoles.remove(roleName)
        await self.config.guild(ctx.guild).roleList.set(currentRoles)
        return True


    # Bot Commands

    @commands.command(name="roles", aliases=["iam"])
    async def wroles(self, ctx, *, role: discord.Role=None):
        """List self-assignable Event Roles
        
        Add roles using `[p]roles roleYouWantToAddHere`"""
        if role == None:
            currentRoles = await self.config.guild(ctx.guild).roleList()
            # [TODO] Create an embed of these roles, with @mentions
            await ctx.send(currentRoles)
        else:
            # [TODO] Add check for if role is in roleList
            await ctx.author.add_roles(role)
            await ctx.message.add_reaction("✅")
    
    @commands.guild_only()
    @commands.group()
    @checks.mod()
    async def setroles(self, ctx: commands.Context):
        """Role management for Trees and Contributor Hub
        
        To list all roles, do `[p]roles`"""
        if not ctx.invoked_subcommand:
            pass

    @setroles.command(name="create")
    async def setrolescreate(self, ctx, *, roleName):
        """Create a pingable Event Role (for Cafe Events and #hangouts)
        
        Please make sure your event shows demonstrated interest first!
        Demonstrated interest can be pre-planned meetups of 5+ users, or at least 3 consecutive events, or some form of community benefit to having a pingable role."""
        
        # [TODO] Add support for await self.wait_for(hex, check=x, timeout=10.0)
        #
        # role = await ctx.guild.create_role(name=roleName, mentionable=True, colour = discord.Colour(int(f"0x{hexColor}", 16)))

        role = await ctx.guild.create_role(name=roleName, mentionable=True)
        await self.addToRoleList(ctx, role)
        await ctx.send(f"{role.mention} is created and ready for use! Add it using `,wroles`")
        
    @setroles.command(name="add")
    @checks.admin()
    async def setrolesadd(self, ctx, *, roleName: discord.Role):
        """Adds an existing role to the list of Event Roles."""
        await self.addToRoleList(ctx, roleName)
        await ctx.message.add_reaction("✅")
        
    @setroles.command(name="remove")
    @checks.admin()
    async def setrolesremove(self, ctx, *, roleName: discord.Role):
        """Removes an existing role from the list of Event Roles."""
        await self.removeFromRoleList(ctx, roleName)
        await ctx.message.add_reaction("✅")
        
    @setroles.command(name="enable")
    @checks.admin()
    async def setrolesenable(self, ctx, *, roleName: discord.Role):
        """Make an Event Role mentionable.
        
        Only for if you've made it unmentionable using disable"""
        await roleName.edit(mentionable=True)
        await ctx.message.add_reaction("✅")
        
    @setroles.command(name="disable")
    @checks.admin()
    async def setrolesdisable(self, ctx, *, roleName: discord.Role):
        """Make an Event Role unmentionable. Does not delete the role."""
        await roleName.edit(mentionable=False)
        await ctx.message.add_reaction("✅")

    @setroles.command(name="edit")
    async def setrolesedit(self, ctx, *, roleName: discord.Role):
        """Edit an Event Role"""
        # [TODO] Add support for await self.wait_for(hex, check=x, timeout=10.0)
