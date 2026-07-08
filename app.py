import asyncio
import os
from bot import bot
import listener.character_info
import listener.help
import listener.sunday
import listener.boutique
import listener.guild_info
from consts.colors import ERROR_COLOR
from consts.command_prefix import COMMAND_PREFIX
from discord.ext import commands
import discord


@bot.event
async def on_ready():
    print('BOT READY')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"도움말은 {COMMAND_PREFIX}도움 또는 {COMMAND_PREFIX}help"), status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error):
    print("존재하지 않는 명령어")
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title=":no_entry: **명령어 입력을 확인하세요**",
            color=ERROR_COLOR
        )

        embed.add_field(
            name="존재하지 않는 명령어입니다.",
            value=f"```{COMMAND_PREFIX}도움 또는 {COMMAND_PREFIX}help를 입력하여 명령어 목록을 확인하세요.```",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    # 나머지 에러는 콘솔에 출력
    raise error


async def main():
    token = os.getenv('DISCORD_BOT_TOKEN')

    print("DISCORD_BOT_TOKEN 존재 여부:")
    print("DISCORD_BOT_TOKEN" in os.environ)

    print("값:")
    print(os.getenv("DISCORD_BOT_TOKEN"))

    print("환경변수 목록:")
    print(list(os.environ.keys()))
    
    if token is None:
        print('토큰이 설정되지 않았습니다.')
        raise RuntimeError("토큰이 없습니다")
    await bot.start(token=token)

asyncio.run(main=main())
