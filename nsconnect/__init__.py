from .nsconnect import NSConnect


def setup(bot):
    bot.add_cog(NSConnect(bot))