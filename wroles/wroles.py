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

        """ concept draft
        "rolelist": [ [role.name, role.mention, role.id], ... ],
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

    async def findRoleFromText(self, ctx, searchtext):
        """Retrieve a role based on searching text"""
        # Retrieve role info
        currentRoles = await self.config.guild(ctx.guild).roleList()
        # Search for role in currentRoles list
        for c in currentRoles:
            # Lowercase everything before searching
            # Breaking abstraction layer, but it's quicker bc we already have the array items
            # Array item format: [role.name, role.mention, role.id]
            if searchtext.lower() in c[0].lower():
                # Return role id if there is match
                return c[2]
            else:
                pass
        return False


    # Bot Commands

    @commands.command(name="roles", aliases=["role", "iam", "am", "iamn", "amn", "iamnot", "amnot"])
    async def wroles(self, ctx, *, role=None):
        """List self-assignable Event Roles
        
        Add roles using `[p]roles roleYouWantToAddHere`"""
        # Get roles
        currentRoles = await self.config.guild(ctx.guild).roleList()
        
        if role == None:
            # If there isn't a role specified, build an embed
            # we get the mentions from each role by running roledataMention for each in currentRoles
            # then we add them to a string with "\n" for newline
            # and then finish by adding a title and footer
            embedList = ""
            for a in currentRoles:
                b = self.roledataMention(a)
                embedList += b+"\n"
            e = discord.Embed(color=(await ctx.embed_colour()), title="Cafe Events Roles", description=embedList)
            e.set_footer(text="Add a role using `,iam rolenamehere`")
            await ctx.send(embed=e)
        else:
            # Call findRoleFromText, which returns role id
            b = await self.findRoleFromText(ctx, role)
            if b == False:
                await ctx.send("Hmmm did you misspell the role? Try just ,iam to see the roles you can add!")
            else:
                # Now that we have the role id, we call .get_role() to get the role
                # and assign it to the user
                c = ctx.guild.get_role(b)
                if c in ctx.author.roles:
                    # User already has role, remove it now
                    await ctx.author.remove_roles(c)
                    await ctx.message.add_reaction("📤")
                else:
                    # User doesn't have role yet, add it now
                    await ctx.author.add_roles(c)
                    # Don't add reaction for joining role, it ended up just being confusing....
                await ctx.message.add_reaction("✅")
    
    @commands.guild_only()
    @commands.group()
    @checks.mod()
    async def setroles(self, ctx: commands.Context):
        """Role management for Trees

        The base commands for this bot are `[p]roles` for users to self-add roles, and `[p]setroles` for Trees to create/manage roles.

        Get started:
        - Create a new role using `[p]setroles create`
        - Customize the color afterwards using `[p]setroles editcolor`
        - List all roles using `[p]roles`

        Aliases:
        - `,wroles`:  `,wrole`  `,iam`
        """
        if not ctx.invoked_subcommand:
            pass

    @setroles.command(name="create")
    async def setrolescreate(self, ctx, *, roleName):
        """Create a pingable Event Role (for Cafe Events and #hangouts)
        
        Please make sure your event shows demonstrated interest first!
        Demonstrated interest can be pre-planned meetups of 5+ users, or at least 3 consecutive events, or some form of community benefit to having a pingable role."""
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
        
    @setroles.command(name="remove")
    async def setrolesremove(self, ctx, *, roleName: discord.Role):
        """Removes an existing role from the list of Event Roles."""
        await self.removeFromRoleList(ctx, roleName)
        await ctx.message.add_reaction("✅")

    @setroles.command(name="update")
    async def setrolesupdate(self, ctx):
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
