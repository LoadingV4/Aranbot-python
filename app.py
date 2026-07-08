import asyncio
import os
from bot import bot
import listener.character_info
import listener.help
import listener.sunday
import listener.boutique
import listener.guild_info
import exceptions.exception_handler
from consts.colors import ERROR_COLOR
from consts.command_prefix import COMMAND_PREFIX
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('BOT READY')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"도움말은 {COMMAND_PREFIX}도움 또는 {COMMAND_PREFIX}help"), status=discord.Status.online)


async def main():
    if token is None:
        print('토큰이 설정되지 않았습니다.')
        raise RuntimeError("토큰이 없습니다")
    await bot.start(token=token)

asyncio.run(main=main())
