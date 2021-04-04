from redbot.core import Config, commands, checks
from redbot.cogs.admin import admin
import asyncio
import aiohttp
import discord
import time

class Wprune(commands.Cog):
    """Wysc Prune Management"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=822775204043948063)
        default_guild = {
            "SeedRole": "",
            "SproutRole": "",
            "OtherRoles": []
        }

        self.config.register_guild(**default_guild)

    async def red_get_data_for_user(self, *, user_id: int):
        return "This cog stores your public Discord User ID for the purposes of maintaining the Wysc service."

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not story any data
        pass


    # Utility Commands

    def getRoleMembers(self, ctx, role: discord.Role):
        return role.members

    def getRoleMembersId(self, ctx, role: discord.Role):
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


    @commands.guild_only()
    @commands.group()
    @checks.admin()
    async def setprune(self, ctx: commands.Context):
        """Set Prune content"""
        if not ctx.invoked_subcommand:
            pass

    @setprune.command(name="seed")
    async def setpruneseed(self, ctx, *, roleId: discord.Role):
        """Set Seed/base role"""
        await self.config.guild(ctx.guild).SeedRole.set(roleId.id)
        await ctx.message.add_reaction("✅")

    @setprune.command(name="sprout")
    async def setprunesprout(self, ctx, *, roleId: discord.Role):
        """Set Sprout/upper role"""
        await self.config.guild(ctx.guild).SproutRole.set(roleId.id)
        await ctx.message.add_reaction("✅")

    @setprune.command(name="other")
    async def setpruneother(self, ctx, role: discord.Role):
        """Set other excluded roles"""
        current = await self.config.guild(ctx.guild).OtherRoles()
        if role.id in current:
            current.remove(role.id)
            await self.config.guild(ctx.guild).OtherRoles.set(current)
            await ctx.send('Updated: Removed```'+str(current)+'```')
        else:
            current.append(role.id)
            await self.config.guild(ctx.guild).OtherRoles.set(current)
            await ctx.send('Updated: Added```'+str(current)+'```')

    @setprune.command(name="list")
    async def setprunelist(self, ctx):
        """List all settings"""
        a = await self.config.guild(ctx.guild).SeedRole()
        b = await self.config.guild(ctx.guild).SproutRole()
        c = await self.config.guild(ctx.guild).OtherRoles()
        await ctx.send('```SeedRole: '+str(a)+'\nSproutRole: '+str(b)+'\nOtherRoles:'+str(c)+'```')

    
    @commands.command()
    @checks.admin()
    async def prunerole(self, ctx, run: bool=False):
        """Start the prune"""
        if run == True:
            # Get role info
            seedroleID = await self.config.guild(ctx.guild).SeedRole()
            sproutroleID = await self.config.guild(ctx.guild).SproutRole()
            otherrolesID = await self.config.guild(ctx.guild).OtherRoles()
            # Get roles
            seedrole = ctx.guild.get_role(seedroleID)
            sproutrole = ctx.guild.get_role(sproutroleID)
            # Get role members
            seeds = self.getRoleMembers(ctx, seedrole)
            sprouts = self.getRoleMembers(ctx, sproutrole)
            others = []
            for i in otherrolesID:
                aa = ctx.guild.get_role(i)
                bb = self.getRoleMembers(ctx, aa)
                others.append(bb)
            # Get difference
            toprune = self.getListDifference(seeds,sprouts)
            for j in others:
                toprune = self.getListDifference(toprune, j)

            # TODO: Add check for member's join date and compare against [days=14]-> timestamp
            
            # TODO: Convert the Addrole into a removerole of seedrole

            # Addrole
            newrole = ctx.guild.get_role(822802611509395466)
            for index, mem in enumerate(toprune, start=1):
                await mem.add_roles(newrole)
                if index % 1 == 0:
                    await ctx.send("{} of {} done".format(index,len(toprune)))
            await ctx.send("Done")
            
        else:
            # Don't run yet
            a = "Are you sure you want to run this command? If you're sure the settings below are correct, start pruning roles by running this command again, followed by `True`"
            await ctx.send(a)
