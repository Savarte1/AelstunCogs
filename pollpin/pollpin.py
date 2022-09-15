from redbot.core import commands, Config
from redbot.core.bot import Red
import discord
from typing import Union, Dict

class PollPin(commands.Cog):
    """A cog to generate pins for voting ballots using forms"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=46_930_395_012, force_registration=True)
        default_guild = {
            "polls": {}
        }
        self.config.register_guild(**default_guild)

    # Helper functions

    async def _pollpin_makepoll(self, guild: discord.Guild, role: discord.Role, author: discord.User, poll: str):
        await self.config.guild(guild).set_raw("polls", poll, value={"role": role.id, "owner": author.id ,"pins": {}}) 
        
    async def _pollpin_exists(self, guild: discord.Guild, poll) -> bool:
        polls = await self.config.guild(guild).polls()
        if (poll in polls):
            return True
        else:
            return False
    
    async def _pollpin_delpoll(self, guild: discord.Guild, poll):
        await self.config.guild(guild).clear_raw("polls", poll)

    def _pollpin_embed(self, **kwargs):
        embedargs = kwargs
        embedargs["title"] = "PollPins"
        embedargs["colour"] = discord.Colour.dark_purple()
        embed = discord.Embed(**embedargs)
        return embed
    
    # Commands

    @commands.command()
    @commands.guild_only()
    async def getpin(self, ctx: commands.Context, pollname: str):
        """Obtain a poll pin"""
        
        await ctx.author.send(f"Your PIN for the {pollname} poll is")
    
    @commands.group()
    @commands.mod()
    @commands.guild_only()
    async def managepoll(self, ctx: commands.Context):
        """Manage polls"""
        pass

    @managepoll.command(name="new")
    async def managepoll_new(self, ctx: commands.Context, poll: str, role: discord.Role):
        """Make new poll"""
        msg = ""
        if not await self._pollpin_exists(ctx.guild, poll):
            await self._pollpin_makepoll(ctx.guild, role, ctx.author, poll)
            msg = f"Made new poll {poll} for role {role.name}"
        else:
            msg = f"{poll} already exists"
        await ctx.send(msg)
    
    @managepoll.command(name="list")
    async def managepoll_list(self, ctx: commands.Context):
        """Get list of polls"""
        embed = self._pollpin_embed(description=f"List of Polls in {ctx.guild}")
        polls = await self.config.guild(ctx.guild).polls()
        if polls:
            msgdict = {"polls": "", "roles": "", "owners": ""}
            for poll, polldata in polls.items():
                role = discord.utils.get(ctx.guild.roles, id=polldata["role"])
                author = self.bot.get_user(polldata["owner"])
                msgdict["polls"] += f"{poll}\n"
                msgdict["roles"] += f"{role}\n"
                msgdict["owners"] += f"{author}\n"
            embed.add_field(name="Poll", value=msgdict["polls"], inline=True)
            embed.add_field(name="Role", value=msgdict["roles"], inline=True)
            embed.add_field(name="Owner", value=msgdict["owners"], inline=True)
        else:
            embed.add_field(name="Notice", value="There are no polls in this server")
        await ctx.send(embed=embed)

    @managepoll.command(name="getpins")
    async def managepoll_getpins(self, ctx: commands.Context, poll: str):
        """Get list of pins from poll"""
        msg = ""
        if await self._pollpin_exists(ctx.guild, poll):
            msg = f"**List of Pins in {poll}:**"
            data = await self.config.guild(ctx.guild).get_raw("polls", poll)
            for pinnumber in data["pins"].values():
                msg += f"\n {pinnumber}"
        else:
            msg = f"{poll} does not exist"
        await ctx.author.send(msg)

    @managepoll.command(name="remove")
    async def managepoll_remove(self, ctx: commands.Context, poll: str):
        """Delete polls"""
        msg = ""
        if await self._pollpin_exists(ctx.guild, poll):
            await self._pollpin_delpoll(ctx.guild, poll)
            msg = f"{poll} has been deleted"
        else:
            msg = f"{poll} does not exist"
        await ctx.send(msg)
