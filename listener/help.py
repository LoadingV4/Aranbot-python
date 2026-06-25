import discord
from bot import bot
from consts.colors import INFO_COLOR
from consts.command_prefix import COMMAND_PREFIX


@bot.command(name="도움", aliases=["도움말"])
async def get_help(ctx):
    await ctx.send(embed=create_help())


def create_help():
    embed = discord.Embed(title=":information: 명령어 목록입니다!", color=INFO_COLOR)
    embed.add_field(
        name=f"1. `{COMMAND_PREFIX}정보 캐릭터명` 또는 `{COMMAND_PREFIX}info 캐릭터명`",
        value="캐릭터의 기본 정보를 표시합니다.",
        inline=False
    )

    embed.add_field(
        name=f"2. `{COMMAND_PREFIX}스탯 캐릭터명` 또는 `{COMMAND_PREFIX}stat 캐릭터명`",
        value="전투력, 보스 공격력 등 캐릭터의 스탯을 표시합니다.",
        inline=False
    )

    embed.add_field(
        name=f"3. `{COMMAND_PREFIX}길드 길드명` 또는 `{COMMAND_PREFIX}guild 길드명`",
        value="길드의 정보를 표시합니다.\n명령어 입력 후 월드를 선택해야 정보가 표시됩니다.",
        inline=False
    )

    embed.add_field(
        name=f"4. `{COMMAND_PREFIX}해방`",
        value="해방 일정을 계산합니다.",
        inline=False
    )

    embed.add_field(
        name=f"5. `{COMMAND_PREFIX}썬데이` 또는 `{COMMAND_PREFIX}선데이` 또는 `{COMMAND_PREFIX}sun`",
        value="공지에 올라온 썬데이 메이플을 알려줍니다.",
        inline=False
    )

    embed.add_field(
        name=f"6. `{COMMAND_PREFIX}문어 (2 ~ 9)` 또는 `{COMMAND_PREFIX}알파카 (2 ~ 9)`",
        value=(
            "알파카 이벤트 시뮬레이션을 하여 당신의 운을 시험해보세요.\n"
            "뒤 숫자는 목표 레벨을 2 ~ 9레벨까지 입력할 수 있고, 생략 가능합니다.\n"
            "생략시 시뮬레이션 100회를 전부 시도하고, "
            "입력시 목표 레벨에 도달하면 시뮬레이션을 중단합니다."
        ),
        inline=False
    )

    embed.add_field(
        name=f"7. `{COMMAND_PREFIX}부티크 개수(1 ~ 10,000,000)`",
        value=(
            "부티크 기프트 시뮬레이션을 실행합니다.\n"
            "뒤에는 정수 형태로 부티크 기프트의 개수를 "
            "1 ~ 10,000,000 범위 내에서 입력해주세요."
        ),
        inline=False
    )

    embed.add_field(
        name=f"8. `{COMMAND_PREFIX}스타포스` 또는 `{COMMAND_PREFIX}별`",
        value="스타포스 시뮬레이션을 실행합니다.\n과연 신창섭께서 당신에게 웃어줄까요?",
        inline=False
    )
    return embed
