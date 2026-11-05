from bot import bot
from service.nexon import *
from consts.colors import INFO_COLOR
import discord


@bot.command(name="스케줄러", aliases=["스케쥴러", "할일", "스케줄"])
async def scheduler(ctx, *, character_name: str):
    ocid = get_ocid(character_name=character_name)
    url = "https://open.api.nexon.com/maplestory/v1/scheduler/character-state?ocid="+ocid
    result = get_info(send_request(url=url))

    await ctx.reply(embed=result)


def get_info(response):
    clear_count = response["weekly_boss_clear_count"]
    limit_count = response["weekly_boss_clear_limit_count"]

    character_name = response["character_name"]
    world_name = response["world_name"]
    character_level = response["character_level"]
    character_class = response["character_class"]

    embed = discord.Embed(
        title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

    weekly_bosses = [boss for boss in response["boss_contents"]
                     if boss["registration_flag"] == "true" and boss["cycle"] == "bossWeekly"]

    print(f"주간 보스({clear_count}/{limit_count}), {weekly_bosses}")
    if clear_count == limit_count and weekly_bosses:
        embed.add_field(
            name="주간 보스", value=f"모두 클리어({clear_count}/{limit_count})✅")
    else:
        difficulty_map = {
            "easy": "이지",
            "normal": "노멀",
            "hard": "하드",
            "chaos": "카오스",
            "extreme": "익스트림"
        }

        boss_list = {}

        for boss in weekly_bosses:
            name = boss["content_name"]
            difficulty = difficulty_map.get(
                boss["difficulty"], boss["difficulty"])

            boss_name = f"{difficulty} {name}"

            status = "✅" if boss["complete_flag"] == "true" else "❌"

            boss_list[boss_name] = status
            embed.add_field(name=boss_name, value=boss_list[boss_name], inline=True)

    return embed
