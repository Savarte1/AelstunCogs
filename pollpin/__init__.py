from .pollpin import PollPin

async def setup(bot):
    await bot.add_cog(PollPin(bot))
