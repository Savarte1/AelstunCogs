from redbot.core import commands, Config
from redbot.core.bot import Red
import discord


class NSConnect(commands.Cog):
    """Verification and role assignment cog for NationStates"""

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=9_472_561_059, force_registration=True
        )
        default_global = {
            "agent": None
        }
        default_guild = {
            "visitor": None,
            "unverified": None,
            "verified": None,
            "wa_member": None,
            "resident": {},
            "lobby": None
        }
        default_member = {
            "exempt": False
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)

    async def initialize(self):
        pass
