from .pollpin import PollPin

async def setup(bot):
    bot.add_cog(PollPin(bot))
