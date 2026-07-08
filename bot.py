import discord
from discord.ext import commands
from consts.command_prefix import COMMAND_PREFIX

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=intents,
    help_command=None
)