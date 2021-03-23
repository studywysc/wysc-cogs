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

    def roledataItem(self, arrayitem):
        return [arrayitem.name, arrayitem.mention, arrayitem.id]

    def roledataName(self, arrayitem):
        return arrayitem[0]

    def roledataMention(self, arrayitem):
        return arrayitem[1]

    def roledataId(self, arrayitem):
        return arrayitem[2]

    async def addToRoleList(self, ctx, roleName: discord.Role):
        """Add a role to the list of roles"""
        # Make sure the name of current roles are updated first (to make sure the sort is correct)
        await self.updateRoleList(ctx)
        # Retrieve role info
        currentRoles = await self.config.guild(ctx.guild).roleList()
        # Append a role item array
        currentRoles.append(self.roledataItem(roleName))
        # Sort the array alphabetically
        currentRoles.sort(key=self.roledataName)
        # Commit the changes to guild data
        await self.config.guild(ctx.guild).roleList.set(currentRoles)

    async def removeFromRoleList(self, ctx, roleName: discord.Role):
        """Remove a role from the list of roles"""
        # Make sure the name of current roles are updated first (otherwise the remove will fail)
        await self.updateRoleList(ctx)
        # Retrieve role info
        currentRoles = await self.config.guild(ctx.guild).roleList()
        # Remove a role item array
        currentRoles.remove(self.roledataItem(roleName))
        # Commit the changes to guild data
        await self.config.guild(ctx.guild).roleList.set(currentRoles)
        
    async def updateRoleList(self, ctx):
        """Updates the role names in the database"""
        # Retrieve role info
        currentRoles = await self.config.guild(ctx.guild).roleList()
        # For each existing item in currentRoles, get fresh data on all of them
        # then append it to sortRoles
        sortRoles = []
        for a in currentRoles:
            b = ctx.guild.get_role(self.roledataId(a))
            sortRoles.append(self.roledataItem(b))
        # Sort the array of items by role name
        sortRoles.sort(key=self.roledataName)
        # Commit the changes to guild data
        await self.config.guild(ctx.guild).roleList.set(sortRoles)
        await ctx.message.add_reaction("✅")


    # Bot Commands

    @commands.command(name="roles", aliases=["iam"])
    async def wroles(self, ctx, *, role: discord.Role=None):
        """List self-assignable Event Roles
        
        Add roles using `[p]roles roleYouWantToAddHere`"""

        # Get roles, then make crList which only has the role id's
        currentRoles = await self.config.guild(ctx.guild).roleList()
        
        if role == None:
            # If there isn't a role specified, build an embed
            # we get the mentions from each role by running roledataMention for each in currentRoles
            # then we add them to a string with "\n" for newline
            embedList = ""
            for a in currentRoles:
                b = self.roledataMention(a)
                crList += b+"\n"
            e = discord.Embed(color=(await ctx.embed_colour()), description=embedList)
            await ctx.send(embed=e)
        else:
            # If there is a role specified, role.id will give us its role id
            # We build crList with a list of role id's
            crList = [self.roledataId(r) for r in currentRoles]
            # If there's a match, we .add_role to them
            if role.id in crList:
                await ctx.author.add_roles(role)
                await ctx.message.add_reaction("✅")
            else:
                await ctx.send("Hmmm did you misspell the role? Try just ,wroles to see the roles you can add!")
    
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

    @setroles.command(name="editname")
    async def srename(self, ctx, roleName: discord.Role, *, newName):
        """Edit Event Role name"""
        try:
            roleName.edit(name=newName)
        except:
            ctx.send("Oops, that didn't work... Maybe something was typed weird?")
        else:
            await ctx.message.add_reaction("✅")

    @setroles.command(name="editcolor", aliases=["editcolour"])
    async def srecolor(self, ctx, *, roleName: discord.Role, hexColor):
        """Edit Event Role color/colour"""
        try:
            roleName.edit(colour=discord.Colour(int(f"0x{hexColor}", 16)))
        except:
            ctx.send("Oops, that didn't work... Maybe something was typed weird?")
        else:
            await ctx.message.add_reaction("✅")

    @setroles.command(name="update")
    async def setrolesupdate(self, ctx, *, roleName: discord.Role):
        """Updates the role names in the database."""
        await self.updateRoleList(ctx)
        await ctx.message.add_reaction("✅")

    # Admin roles only    
        
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
        
    @setroles.command(name="reset")
    @checks.admin()
    async def setrolesreset(self, ctx):
        """Reset all of a server's configurations."""
        await self.config.guild(ctx.guild).roleList.set([])
        await self.config.guild(ctx.guild).roleMsgs.set([])
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
