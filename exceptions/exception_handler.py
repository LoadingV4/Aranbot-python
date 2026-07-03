import discord
from bot import bot
from discord.ext import commands
from consts.colors import ERROR_COLOR


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=":no_entry: **명령어 입력을 확인하세요**", color=ERROR_COLOR)
        embed.add_field(name="인수가 필요한 명령어입니다.",
                        value="```!도움 또는 !help를 입력하여 올바른 명령어 형식을 확인하세요.```", inline=False)
        await ctx.send(embed=embed)
