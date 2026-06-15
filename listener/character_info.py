import discord
from bot import bot
from service.nexon import *
from datetime import datetime, date
from consts.colors import *


def get_ocid(character_name):
    response = nexon_request(
        "https://open.api.nexon.com/maplestory/v1/id?character_name=" + character_name)
    if response.ok:
        return response.json().get("ocid")
    else:
        return response.json().get("error")


@bot.command(name="정보", aliases=["info"])
async def info(ctx, *, character_name: str):
    print(f"캐릭터 닉네임 : {character_name}")
    ocid = get_ocid(character_name)
    print(f"ocid : {ocid}")
    if ocid:
        url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
        response = nexon_request(url)
        character_info = get_character_info(response_json=response.json())
        embed = discord.Embed(
            title=f"Lv.{character_info['character_level']} {character_info['character_name']}", color=INFO_COLOR)
        embed.set_image(url=character_info["thumbnail_url"])
        embed.add_field(
            name="직업", value=character_info["character_class"], inline=False)
        embed.add_field(
            name="길드", value=character_info["character_guild_name"], inline=False)
        embed.add_field(
            name="월드", value=character_info["world_name"], inline=False)
        embed.add_field(
            name="전직 차수", value=character_info["character_class_level"], inline=False)
        embed.add_field(
            name="데스티니 해방", value=character_info["liberation_quest_clear"], inline=False)
        embed.add_field(name="최근 7일간 접속 여부",
                        value=character_info["access_flag"], inline=False)
        embed.add_field(
            name="캐릭터 생성일", value=f"{character_info['character_date_create']}(D+{character_info['creation_to_now_days']})", inline=False)
        embed.add_field(
            name="성별", value=character_info["character_gender"], inline=False)
        embed.add_field(
            name="현재 경험치", value=f"{character_info["character_exp_rate"]}%", inline=False)
        await ctx.send(embed=embed)


def get_character_info(response_json):
    character_date_create = datetime.fromisoformat(
        response_json.get("character_date_create").replace("Z", "+00:00")
    ).date()

    return {
        "character_name": response_json.get("character_name"),
        "world_name": response_json.get("world_name"),
        "character_gender": "남:male_sign:" if response_json.get("character_gender") == "남" else "여:female_sign:",
        "character_class": response_json.get("character_class"),
        "character_exp_rate": response_json.get("character_exp_rate"),
        "thumbnail_url": response_json.get("character_image"),
        "character_guild_name": response_json.get("character_guild_name", "소속 길드 없음:x:"),
        "character_class_level": f"{response_json.get('character_class_level')}차",
        "liberation_quest_clear": ":white_check_mark:" if response_json.get("liberation_quest_clear") == "2" else ":x:",
        "access_flag": ":white_check_mark:" if response_json.get("access_flag") == "true" else ":x:",
        "character_level": int(response_json.get("character_level")),
        "character_date_create": character_date_create.strftime('%Y년 %m월 %d일'),
        "creation_to_now_days": (date.today() - character_date_create).days,
    }
