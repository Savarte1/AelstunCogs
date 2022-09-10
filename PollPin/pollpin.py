from redbot.core import commands

class PollPin(commands.Cog):
    """A cog to allow pins for voting ballots using forms"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")