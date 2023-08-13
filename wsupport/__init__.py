from .wsupport import wsupport

async def setup(bot):
    await bot.add_cog(wsupport())
