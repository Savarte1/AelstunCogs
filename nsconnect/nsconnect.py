from redbot.core import commands, Config
from redbot.core.bot import Red
import discord


class NSConnect(commands.Cog):

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=9_121_137_209, force_registration=True)
        default_global = {
            "verify_key": ""
        }
        default_user = {
            "nations": {}
        }
        default_guild = {
            "activate": False,
            "unverified_role": None,
            "verified_role": None,
            "resident_roles": None,
            "visitor_role": None
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_user)
        self.config.register_guild(**default_guild)