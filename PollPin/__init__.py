from .pollpin import PollPin


def setup(bot):
    bot.add_cog(PollPin(bot))