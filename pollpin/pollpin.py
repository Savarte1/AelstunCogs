from redbot.core import commands, Config
from redbot.core.bot import Red
import discord
import secrets


class PollPin(commands.Cog):
    """A cog to generate pins for voting ballots using forms"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=46_930_395_012, force_registration=True)
        default_guild = {
            "polls": {}
        }
        self.config.register_guild(**default_guild)

    # Helper functions

    async def _pollpin_makepoll(self, guild: discord.Guild, role: discord.Role, author: discord.User, poll: str):
        await self.config.guild(guild).set_raw("polls", poll, value={"role": role.id, "owner": author.id, "pins": {}})

    async def _pollpin_exists(self, guild: discord.Guild, poll) -> bool:
        polls = await self.config.guild(guild).polls()
        if poll in polls:
            return True
        else:
            return False

    async def _pollpin_delpoll(self, guild: discord.Guild, poll):
        await self.config.guild(guild).clear_raw("polls", poll)

    async def _pollpin_getpin(self, guild: discord.Guild, user: discord.Member, poll: str):
        data = await self.config.guild(guild).get_raw("polls", poll, "pins")
        if str(user.id) in data:
            return data[str(user.id)]
        else:
            pin = secrets.randbelow(1_000_000)
            while self._pollpin_checkdupl(data, pin):
                pin = secrets.randbelow(1_000_000)
            await self.config.guild(guild).set_raw("polls", poll, "pins", user.id, value=pin)
            return pin

    @staticmethod
    def _pollpin_checkdupl(data, checkval):
        for value in data.values():
            if checkval == value:
                return True
        return False

    @staticmethod
    def _pollpin_embed(**kwargs):
        embedargs = kwargs
        embedargs["title"] = "PollPins"
        embedargs["colour"] = discord.Colour.dark_purple()
        embed = discord.Embed(**embedargs)
        return embed

    # Commands

    @commands.command()
    @commands.guild_only()
    async def getpin(self, ctx: commands.Context, poll: str):
        """Obtain a poll pin"""
        if await self._pollpin_exists(ctx.guild, poll):
            data = await self.config.guild(ctx.guild).get_raw("polls", poll)
            role = discord.utils.get(ctx.guild.roles, id=data["role"])
            if role in ctx.author.roles:
                pin = await self._pollpin_getpin(ctx.guild, ctx.author, poll)
                await ctx.send("Your PIN has been sent via DM")
                await ctx.author.send(f"Your PIN for the {poll} poll in {ctx.guild} is {pin}")
            else:
                await ctx.send("You do not have the proper role for this poll")
        else:
            await ctx.send(f"{poll} does not exist")

    @commands.group()
    @commands.guild_only()
    async def managepoll(self, ctx: commands.Context):
        """Manage polls"""
        pass

    @commands.admin()
    @managepoll.command(name="new")
    async def managepoll_new(self, ctx: commands.Context, poll: str, role: discord.Role):
        """Make new poll"""
        if not await self._pollpin_exists(ctx.guild, poll):
            await self._pollpin_makepoll(ctx.guild, role, ctx.author, poll)
            await ctx.send(f"Made new poll {poll} for role {role.name}")
        else:
            await ctx.send(f"{poll} already exists")

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

    @managepoll.command(name="info")
    async def managepoll_info(self, ctx: commands.Context, poll: str):
        """Get info about a specific poll"""
        if await self._pollpin_exists(ctx.guild, poll):
            data = await self.config.guild(ctx.guild).get_raw("polls", poll)
            role = discord.utils.get(ctx.guild.roles, id=data["role"])
            author = self.bot.get_user(data["owner"])
            embed = self._pollpin_embed(description=f"Information on {poll} in {ctx.guild}")
            embed.add_field(name="Role", value=str(role), inline=True)
            embed.add_field(name="Owner", value=str(author), inline=True)
            embed.add_field(name="Pins",
                            value=f"Use {ctx.clean_prefix}managepoll pins [poll] to get pins",
                            inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{poll} does not exist")

    @managepoll.command(name="pins")
    async def managepoll_pins(self, ctx: commands.Context, poll: str):
        """Get pins from poll"""
        if await self._pollpin_exists(ctx.guild, poll):
            data = await self.config.guild(ctx.guild).get_raw("polls", poll)
            if ctx.author.id == data["owner"]:
                pinlist = ""
                for pin in data["pins"].values():
                    pinlist += f"{pin}\n"
                if not pinlist:
                    pinlist = f"No pins in {poll} at {ctx.guild}"
                embed = self._pollpin_embed(description=f"Pins in {poll} at {ctx.guild}")
                embed.add_field(name="Pins", value=pinlist, inline=False)
                await ctx.send(f"The PINs for {poll} have been sent via DM")
                await ctx.author.send(embed=embed)
            else:
                await ctx.send(f"You may not view the pins for {poll} as you are not the poll owner")
        else:
            await ctx.send(f"{poll} does not exist")

    @commands.admin()
    @managepoll.command(name="remove")
    async def managepoll_remove(self, ctx: commands.Context, poll: str):
        """Delete polls"""
        if await self._pollpin_exists(ctx.guild, poll):
            await self._pollpin_delpoll(ctx.guild, poll)
            await ctx.send(f"{poll} has been deleted")
        else:
            await ctx.send(f"{poll} does not exist")
