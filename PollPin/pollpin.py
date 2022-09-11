from redbot.core import commands
from redbot.core import Config
from redbot.core.bot import Red
import discord

class PollPin(commands.Cog):
    """A cog to generate pins for voting ballots using forms"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=46_930_395_012, force_registration=True)
        default_member = {
            "pincodes": {}
        }
        default_guild = {
            "polls": {}
        }
        self.config.register_member(**default_member)
        self.config.register_guild(**default_guild)

    @commands.command()
    async def getpin(self, ctx: commands.Context, pollname: str):
        """Obtain a poll pin"""
        
        await ctx.author.send("Your PIN for the " + pollname + "poll is")
    
    @commands.command()
    @commands.mod
    async def mkpoll(self, ctx: commands.Context, pollname: str, role: discord.Role):
        """Make new poll"""
        async with self.config.guild(ctx.guild).polls() as polls:
            polls[pollname] = {"role": role.id, "pins": {}}
        await ctx.send("Made new poll " + pollname + "for role" + role.name)