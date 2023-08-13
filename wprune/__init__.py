from .wprune import Wprune

async def setup(bot):
    await bot.add_cog(Wprune())
