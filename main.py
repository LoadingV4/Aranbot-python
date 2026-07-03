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

token = os.getenv('DISCORD_BOT_PYTHON_TOKEN')


@bot.event
async def on_ready():
    print('BOT READY')


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
        # await bot.process_commands(message)
        await ctx.send(embed=embed)
        return

    # 나머지 에러는 콘솔에 출력
    raise error


async def main():
    if token is None:
        print('토큰이 설정되지 않았습니다.')
        raise RuntimeError("토큰이 없습니다")
    print(bot.commands)
    await bot.start(token=token)

asyncio.run(main=main())
