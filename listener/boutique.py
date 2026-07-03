import random
import discord
from bot import bot
from consts.colors import GOLD_COLOR, ERROR_COLOR

NORMAL_RATES = [
    (0.4994, 1),
    (0.8494, 2),      # 0.4994 + 0.35
    (0.9494, 4),      # +0.1
    (0.9894, 6),      # +0.04
    (0.9964, 10),     # +0.007
    (0.9994, 50),     # +0.003
    (0.9997, 100),    # +0.0003
    (0.9999, 500),    # +0.0002
    (1.0, 1000),      # +0.0001
]

FEVER_RATES = [
    (0.9494, 4),
    (0.9894, 6),
    (0.9964, 10),
    (0.9994, 50),
    (0.9997, 100),
    (0.9999, 500),
    (1.0, 1000),
]


@bot.command(name="부티크")
async def boutique(ctx, *, amount: str):
    print(f"부티크 : {amount}개")
    if not amount.isdigit() or int(amount) > 10000000:
        embed = discord.Embed(
            title=":no_entry: **명령어 입력을 확인하세요**", color=ERROR_COLOR)
        embed.add_field(name="인수가 필요한 명령어입니다.",
                        value="```!도움 또는 !help를 입력하여 올바른 명령어 형식을 확인하세요.```", inline=False)
        await ctx.send(embed=embed)
        return
    
    await ctx.send(embed=get_boutique_embed(int(amount)))


def draw(rates):
    seed = random.random()  # 0.0 <= seed < 1.0

    for rate, tickets in rates:
        if seed < rate:
            return tickets

    return rates[-1][1]


def get_ticket(total_attempts):
    total_ticket = 0
    fever_ticket = 0
    normal_ticket = 0

    for i in range(1, total_attempts + 1):
        is_fever = (i % 10 == 0)

        got = draw(FEVER_RATES if is_fever else NORMAL_RATES)

        total_ticket += got

        if is_fever:
            fever_ticket += got
        else:
            normal_ticket += got

    return total_ticket, fever_ticket, normal_ticket


def get_boutique_embed(total):
    total_ticket, fever_ticket, normal_ticket = get_ticket(total)

    average = total_ticket / total
    print(f"평균 : {average}")
    embed = discord.Embed(
        title="🎁 부티크 시뮬레이션 결과",
        color=GOLD_COLOR
    )

    embed.add_field(
        name=f"👏 {total:,}개를 까서 총 {total_ticket:,}개가 나왔습니다!",
        value=(
            "📊 **상세 결과**\n"
            "```"
            f"일반 획득 개수 : {normal_ticket:,}개\n\n"
            f"피버타임 획득 개수 : {fever_ticket:,}개\n\n"
            f"1회당 평균 획득 개수 : {average:.2f}개"
            "```"
        ),
        inline=False
    )

    return embed
