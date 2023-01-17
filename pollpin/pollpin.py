from redbot.core import commands, Config, data_manager
from redbot.core.bot import Red
import discord
from databases import Database
import secrets
from typing import Optional
import asyncio
from .queries import *


class PollPin(commands.Cog):
    """A cog to generate pins for voting ballots using forms"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=46_930_395_012, force_registration=True
        )
        self.database: Optional[Database] = None
        asyncio.create_task(self.initialize())
    async def initialize(self):
        dbpath = data_manager.cog_data_path(self) / "pollpin.db"
        self.database = Database(f"sqlite://{dbpath}")
        await self.database.connect()
        await self.database.execute(query=POLLPIN_DB_INIT)

    def cog_unload(self):
        asyncio.create_task(self.database.disconnect())

    @staticmethod
    def _pollpin_embed(**kwargs):
        embed_args = kwargs
        embed_args["title"] = "PollPins"
        embed_args["colour"] = discord.Colour.dark_purple()
        embed = discord.Embed(**embed_args)
        return embed

    # Commands

    @commands.command()
    @commands.guild_only()
    async def getpin(self, ctx: commands.Context, poll: str):
        """Obtain a poll pin"""
        pass

    @commands.group()
    @commands.guild_only()
    async def managepoll(self, ctx: commands.Context):
        """Manage polls"""
        pass

    @commands.admin()
    @managepoll.command(name="new")
    async def managepoll_new(
        self, ctx: commands.Context, poll: str, role: discord.Role
    ):
        """Make new poll"""
        pass

    @managepoll.command(name="list")
    async def managepoll_list(self, ctx: commands.Context):
        """Get list of polls"""
        pass

    @managepoll.command(name="info")
    async def managepoll_info(self, ctx: commands.Context, poll: str):
        """Get info about a specific poll"""
        pass

    @managepoll.command(name="pins")
    async def managepoll_pins(self, ctx: commands.Context, poll: str):
        """Get pins from poll"""
        pass

    @commands.admin()
    @managepoll.command(name="remove")
    async def managepoll_remove(self, ctx: commands.Context, poll: str):
        """Delete polls"""
        pass