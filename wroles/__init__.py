from .wroles import wroles

async def setup(bot):
    await bot.add_cog(wroles())
