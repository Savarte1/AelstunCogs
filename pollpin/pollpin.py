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
    @commands.guild_only()
    async def getpin(self, ctx: commands.Context, pollname: str):
        """Obtain a poll pin"""
        
        await ctx.author.send("Your PIN for the " + pollname + "poll is")
    
    @commands.group()
    @commands.mod()
    @commands.guild_only()
    async def managepoll(self, ctx: commands.Context):
        """Manage polls"""
        pass

    @managepoll.command(name="new")
    async def managepoll_new(self, ctx: commands.Context, pollname: str, role: discord.Role):
        """Make new poll"""
        msg = ""
        async with self.config.guild(ctx.guild).polls() as polls:
            if not (pollname in polls):
                polls[pollname] = {"role": role.id, "pins": {}}
                msg = f"Made new poll {pollname} for role {role.name}"
            else:
                msg = f"{pollname} already exists"
        await ctx.send(msg)
    
    @managepoll.command(name="list")
    async def managepoll_list(self, ctx: commands.Context):
        msg = "**List of Polls and assigned Roles**"
        async with self.config.guild(ctx.guild).polls() as polls:
            for pollname, polldict in polls.items():
                discord.utils.get(ctx.guild.roles, id=polldict["role"])
                msg += f"\n{pollname}"
        ctx.send(msg)

    @managepoll.command(name="getpins")
    async def managepoll_getpins(self, ctx: commands.Context, pollname: str):
        """Get list of pins from poll"""
        async with self.config.guild(ctx.guild).polls() as polls:
            if (pollname in polls):
                msg = f"**List of Pins in {pollname}:**"
                for pinnumber in polls[pollname]["pins"].values():
                    msg += f"\n {pinnumber}"
            else:
                msg = f"{pollname} does not exist"
        await ctx.send(msg)

    @managepoll.command(name="remove")
    async def managepoll_remove(self, ctx: commands.Context, pollname: str):
        async with self.config.guild(ctx.guild).polls() as polls:
            if polls.pop(pollname, None):
                msg = f"Poll {pollname} has been deleted"
            else:
                msg = f"{pollname} does not exist"
        ctx.send(msg)
