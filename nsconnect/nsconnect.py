from redbot.core import commands, Config, data_manager, version_info as red_version
from redbot.core.utils import chat_formatting
from redbot.core.bot import Red
from typing import Optional
from pytz import utc
import discord
import hashlib
import aiohttp
import asyncio
import aiofiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiolimiter import AsyncLimiter


class NoAgentException(Exception):
    """Raised when no user agent is set"""

    pass


class NSConnectionError(Exception):
    """Raised when there is an error connecting to NationStates"""

    pass


class NSConnect(commands.Cog):
    """ """

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=9_121_137_209, force_registration=True
        )
        self.nslimiter = AsyncLimiter(40, 30)  # Limit to 40 requests per 30 seconds
        self.nsagent: Optional[str] = None
        self.session = aiohttp.ClientSession()
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.trigger: Optional[CronTrigger] = None
        default_global = {"verify_key": None, "agent": None}
        default_user = {"nations": []}
        default_guild = {
            "activate": False,
            "unverified_role": None,
            "verified_role": None,
            "resident_roles": {},
            "wa_member_role": None,
            "visitor_role": None,
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_user)
        self.config.register_guild(**default_guild)
        asyncio.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_red_ready()
        agent = await self.config.agent()
        if agent:
            self.nsagent = f"{agent} Red-DiscordBot/{red_version}"

        # Scheduler
        self.scheduler = AsyncIOScheduler(timezone=utc)
        self.trigger = CronTrigger(hour=7, second=30)
        self.scheduler.add_job(self._nsupdate(), self.trigger)
        self.scheduler.start()

    def cog_unload(self):
        if self.scheduler:
            self.scheduler.shutdown()
        asyncio.create_task(self.session.close())

    # Helper Functions

    async def _get_token(self, nation: str):
        key = await self.config.verify_key()
        if key:
            nation_hash = hashlib.sha256(nation).hexdigest()
            raw_token = f"{key}{nation_hash}"
            return hashlib.sha256(raw_token).hexdigest()
        else:
            return None

    async def _nsrequest(self, uri: str, data=False):
        if not self.nsagent:
            raise NoAgentException
        headers = {"User-Agent": f"{self.nsagent}"}
        compiled_uri = f"https://www.nationstates.net/{uri}"
        async with self.nslimiter:
            async with self.session.get(compiled_uri, headers=headers) as response:
                if response.status == 200:
                    if data:
                        return await response.read()
                    else:
                        return await response.text()
                else:
                    raise NSConnectionError

    async def _nsdump(self):
        if not self.nsagent:
            raise NoAgentException
        uri = "pages/nations.xml.gz"
        data_directory = data_manager.cog_data_path(self)
        path = data_directory / "nations.xml.gz"
        try:
            dump = await self._nsrequest(uri, data=True)
        except NSConnectionError:
            raise NSConnectionError
        else:
            async with aiofiles.open(path, mode="wb") as f:
                await f.write(dump)

    # Updater

    async def _nsupdate(self):
        if not self.nsagent:
            return

        try:
            await self._nsdump()
        except NSConnectionError:
            return

    # Commands

    @commands.admin()
    @commands.guild_only()
    @commands.group()
    async def nsrole(self, ctx: commands.Context):
        pass

    @nsrole.command(name="verified")
    async def nsrole_verified(self, ctx: commands.Context, role: discord.Role = None):
        if role:
            await self.config.verified_role.set(role.id)
            await ctx.send(f"Set verified role to {role}")
        else:
            await self.config.verified_role.clear()

    @nsrole.command(name="unverified")
    async def nsrole_unverified(self, ctx: commands.Context, role: discord.Role = None):
        if role:
            await self.config.unverified_role.set(role.id)
            await ctx.send(f"Set unverified role to {role}")
        else:
            await self.config.unverified_role.clear()

    @nsrole.command(name="visitor")
    async def nsrole_visitor(self, ctx: commands.Context, role: discord.Role = None):
        if role:
            await self.config.verified_role.set(role.id)
            await ctx.send(f"Set visitor role to {role}")
        else:
            await self.config.verified_role.clear()

    @commands.is_owner()
    @commands.group()
    async def nspanel(self, ctx: commands.Context):
        pass

    @nspanel.command(name="test")
    async def nspanel_test(self, ctx: commands.Context, uri):
        """Test requests"""
        try:
            req = await self._nsrequest(uri)
        except NoAgentException:
            await ctx.send("User agent not set")
        except NSConnectionError:
            await ctx.send("Error connecting to NationStates")
        else:
            await ctx.send(chat_formatting.box(req, "xml"))

    @nspanel.command(name="getdump")
    async def nspanel_getdump(self, ctx: commands.Context):
        """Download NS Nations dump"""
        try:
            await self._nsdump()
        except NoAgentException:
            await ctx.send("User agent not set")
        except NSConnectionError:
            await ctx.send("Error connecting to NationStates")
        else:
            await ctx.send("Downloaded NS nations dump")

    @nspanel.command(name="agent")
    async def nspanel_agent(self, ctx: commands.Context, agent: str = None):
        """
        Set user agent

        Make sure to read https://www.nationstates.net/pages/api.html#terms
        The functions of this cog will not work without a set user agent
        """
        if agent:
            await self.config.agent.set(agent)
            self.nsagent = f"{agent} Red-DiscordBot/{red_version}"
            await ctx.send(f"Set user agent to: {agent}")
        else:
            get_agent = await self.config.agent()
            if get_agent:
                await ctx.send(f"The current user agent is: {get_agent}")
            else:
                await ctx.send("No user agent has been set")

    @commands.dm_only()
    @nspanel.command(name="key")
    async def nspanel_key(self, ctx: commands.Context, key: str):
        """
        Set verification key

        This command can only be used in DMs for security reasons
        The key should never be public
        """
        await self.config.verify_key.set(key)
        await ctx.send(f"Set verification key to: {key}")
