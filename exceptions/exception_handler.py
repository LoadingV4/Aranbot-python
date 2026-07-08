import discord
from bot import bot
from discord.ext import commands
from consts.colors import ERROR_COLOR
from consts.command_prefix import COMMAND_PREFIX


@bot.event
async def on_command_error(ctx, error):
    print(f'오류 발생 : {error}')
    if isinstance(error, commands.CommandNotFound):
        print("존재하지 않는 명령어")
        embed = discord.Embed(
            title=":no_entry: **명령어 입력을 확인하세요**",
            color=ERROR_COLOR
        )

        embed.add_field(
            name="존재하지 않는 명령어입니다.",
            value=f"```{COMMAND_PREFIX}도움 또는 {COMMAND_PREFIX}help를 입력하여 명령어 목록을 확인하세요.```",
            inline=False
        )
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        print('잘못된 인수')
        embed = discord.Embed(
            title=":no_entry: **명령어 입력을 확인하세요**", color=ERROR_COLOR)
        embed.add_field(name="인수가 필요한 명령어입니다.",
                        value="```!도움 또는 !help를 입력하여 올바른 명령어 형식을 확인하세요.```", inline=False)

    await ctx.reply(embed=embed)
    return
    # 나머지 에러는 콘솔에 출력
    # raise error
