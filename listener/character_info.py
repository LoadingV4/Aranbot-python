import discord
from bot import bot
from service.nexon import *
from datetime import datetime, date
from consts.colors import INFO_COLOR, ERROR_COLOR


def get_ocid(character_name):
    url = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + character_name
    response = send_request(url)
    if response.ok:
        return response.json().get("ocid")
    else:
        return response.json().get("error")


@bot.command(name="정보", aliases=["info"])
async def info(ctx, *, character_name: str):
    print(f"캐릭터 닉네임 : {character_name}")
    embed = None
    if check_nickname(character_name=character_name):
        try:
            ocid = get_ocid(character_name)
            print(f"ocid : {ocid}")

            url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
            response = send_request(url)
            character_info = get_character_info(response_json=response)
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
        except RuntimeError:
            embed = discord.Embed(title=":no_entry: **에러**", color=ERROR_COLOR)
            embed.add_field(name="알 수 없는 오류입니다.",
                            value="```나중에 다시 시도해주세요.```", inline=False)
        except ForbiddenOperation:
            embed = discord.Embed(title=":no_entry: **에러**", color=ERROR_COLOR)
            embed.add_field(name="현재 할 수 없는 명령입니다.",
                            value="```나중에 다시 시도해주세요.```", inline=False)
        except InvalidIdentifier:
            embed = discord.Embed(
                title=":no_entry: **마지막 접속일로부터 너무 오래되어 조회에 실패했습니다.**", color=ERROR_COLOR)
            embed.add_field(name="조회를 위해 접속일을 갱신해주세요.",
                            value=f"```입력한 닉네임 : {character_name}```", inline=False)
        except CharacterNotFound:
            embed = discord.Embed(
                title=":no_entry: **존재하지 않는 캐릭터입니다.**", color=ERROR_COLOR)
            embed.add_field(name="다른 닉네임을 시도해주세요.",
                            value=f"```입력한 닉네임 : {character_name}```", inline=False)
        # except InvalidApiKey:
        #     pass
        # except InvalidGame:
        #     pass
        except ApiExceed:
            embed = discord.Embed(
                title=":no_entry: **API한도 초과!**", color=ERROR_COLOR)
            embed.add_field(name="더 이상 사용할 수 없습니다!",
                            value="```금일 API한도를 초과하여 사용할 수 없는 명령어입니다.\n내일 다시 사용해주세요.```", inline=False)
        except IllegalStateException:
            embed = discord.Embed(
                title=":no_entry: **API 에러**", color=ERROR_COLOR)
            embed.add_field(name="사용할 수 없습니다.",
                            value="```현재 사용할 수 없는 API입니다.```", inline=False)
        except GameMaintenance:
            embed = discord.Embed(
                title=":no_entry: **메이플스토리 점검중**", color=ERROR_COLOR)
            embed.add_field(name=":tools:현재 게임이 점검중입니다!",
                            value="```점검 중에는 사용할 수 없는 명령어입니다.```", inline=False)
        except ApiMaintenance:
            embed = discord.Embed(
                title=":no_entry: **API 점검중**", color=ERROR_COLOR)
            embed.add_field(name=":tools:현재 API 점검중입니다!",
                            value="```점검 중에는 사용할 수 없는 명령어입니다.```", inline=False)
    else:
        print("유효하지 않은 닉네임")
        embed = discord.Embed(
            title=":no_entry: **유효하지 않은 닉네임입니다.**", color=ERROR_COLOR)
        embed.add_field(name="다른 닉네임을 시도해주세요.",
                        value=f"```입력한 닉네임 : {character_name}\n\n1. 닉네임은 6글자 제한입니다.(영문과 숫자는 한 글자당 0.5글자)\n2. 특수문자 또는 한글 모음, 자음 단독으로는 사용할 수 없습니다.```", inline=False)
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


def check_nickname(character_name):
    hangul = 0
    english = 0
    num = 0
    nickname_minimum = 2
    nickname_limit = 6

    for c in character_name:
        code = ord(c)
        is_special_letter = code <= 47 or 58 <= code <= 64 or 91 <= code <= 96 or 123 <= code <= 127
        is_consonant = 12593 <= code <= 12622
        is_vowel = 12623 <= code <= 12643

        if is_special_letter or is_consonant or is_vowel:
            return False
        if 65 <= code <= 90 or 97 <= code <= 122:
            english += 1
        elif 44032 <= code <= 55203:
            hangul += 1
        else:
            num += 1

    if english == 0 and num == 0:
        return nickname_minimum <= hangul <= nickname_limit
    else:
        return hangul + (english + num) // 2 <= nickname_limit
