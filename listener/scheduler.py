from bot import bot
from service.nexon import *
from consts.colors import INFO_COLOR
import discord
import Paginator


@bot.command(name="스케줄러", aliases=["스케쥴러", "할일", "스케줄"])
async def scheduler(ctx, *, character_name: str):
    ocid = get_ocid(character_name=character_name)
    url = "https://open.api.nexon.com/maplestory/v1/scheduler/character-state?ocid="+ocid
    embed = generate_embed(send_request(url=url))

    await ctx.reply(embed=embed)


def generate_embed(response):
    embeds = []
    pass


def get_weekly_boss(response):
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

    if not weekly_bosses:
        embed.add_field(
            name=f"😈주간 보스({clear_count}/12)", value="아직 보스를 돌지 않았거나 등록된 보스가 없습니다.❌")
    elif clear_count == limit_count:
        embed.add_field(
            name=f"😈주간 보스({clear_count}/{limit_count})", value=f"모두 클리어({clear_count}/{limit_count})✅")
    else:
        difficulty_map = {
            "easy": "이지",
            "normal": "노멀",
            "hard": "하드",
            "chaos": "카오스",
            "extreme": "익스트림"
        }

        boss_list = {}
        embed.add_field(
            name=f"😈주간 보스({clear_count}/{limit_count})", value="", inline=False)
        for boss in weekly_bosses:
            name = boss["content_name"]

            if name == "선택받은 세렌":
                name = "세렌"
            elif name == "감시자 칼로스":
                name = "칼로스"
            elif name == "찬란한 흉성":
                name = "흉성"

            difficulty = difficulty_map.get(
                boss["difficulty"], boss["difficulty"])

            boss_name = f"{difficulty} {name}"

            status = "✅" if boss["complete_flag"] == "true" else "❌"

            boss_list[boss_name] = status
            embed.add_field(
                name=boss_name, value=boss_list[boss_name], inline=True)

    return embed


def get_daily_quests(response):
    character_name = response["character_name"]
    world_name = response["world_name"]
    character_level = response["character_level"]
    character_class = response["character_class"]

    embed = discord.Embed(
        title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

    daily_contents = [content for content in response["daily_contents"]
                      if content["registration_flag"] == "true"]
    if daily_contents:
        daily_list = []
        for content in daily_contents:
            quest = ""
            # monster_park = ""

            # yeoro = ""
            # chuchu = ""
            # lacheln = ""
            # arcana = ""
            # moras = ""
            # esfera = ""
            # moon_bridge = ""
            # labyrinth = ""
            # limen = ""

            # cernium = ""
            # hotel_arcs = ""
            # audium = ""
            # dowonkyung = ""
            # arteria = ""
            # carcion = ""
            # tallahart = ""
            # geardrak = ""

            match content["content_name"]:
                case "몬스터파크":
                    now_count = content["now_count"]
                    max_count = content["max_count"]
                    # monster_park = f"몬파({now_count}/{max_count})"
                    # quest = f"몬파({now_count}/{max_count})"
                    embed.add_field(
                        name="몬파", value=f"몬파({now_count}/{max_count})", inline=False)

                case "[일일 퀘스트] 소멸의 여로 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # yeoro = f"여로 {status}"
                    quest = f"여로 {status}"

                case "[일일 퀘스트] 츄츄 아일랜드 최고의 요리":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # chuchu = f"츄츄 {status}"
                    quest = f"츄츄 {status}"
                case "[일일 퀘스트] 레헬른의 평온한 밤":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # lacheln = f"레헬른 {status}"
                    quest = f"레헬른 {status}"
                case "[일일 퀘스트] 아르카나의 평온한 바람":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # arcana = f"아르카나 {status}"
                    quest = f"아르카나 {status}"
                case "[일일 퀘스트] 모라스의 안정을 위해":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # moras = f"모라스 {status}"
                    quest = f"모라스 {status}"
                case "[일일 퀘스트] 에스페라 연구 명령":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # esfera = f"에스페라 {status}"
                    quest = f"에스페라 {status}"
                case "[일일 퀘스트] 문브릿지 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # moon_bridge = f"문브릿지 {status}"
                    quest = f"문브릿지 {status}"
                case "[일일 퀘스트] 고통의 미궁 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # labyrinth = f"미궁 {status}"
                    quest = f"미궁 {status}"
                case "[일일 퀘스트] 리멘 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # limen = f"리멘 {status}"
                    quest = f"리멘 {status}"

                case "[일일 퀘스트] 세르니움 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # cernium = f"세르니움 {status}"
                    quest = f"세르니움 {status}"
                case "[일일 퀘스트] 호텔 아르크스 주변 청소":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # hotel_arcs = f"호텔 아르크스 {status}"
                    quest = f"호텔 아르크스 {status}"
                case "[일일 퀘스트] 오디움 일대 탐사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # audium = f"오디움 {status}"
                    quest = f"오디움 {status}"
                case "[일일 퀘스트] 도원경 오염 정화":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # dowonkyung = f"도원경 {status}"
                    quest = f"도원경 {status}"
                case "[일일 퀘스트] 아르테리아 잔당 처치":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # arteria = f"아르테리아 {status}"
                    quest = f"아르테리아 {status}"
                case "[일일 퀘스트] 카르시온 복구 지원":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # carcion = f"카르시온 {status}"
                    quest = f"카르시온 {status}"
                case "[일일 퀘스트] 탈라하트 고대신의 힘 조사":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # tallahart = f"탈라하트 {status}"
                    quest = f"탈라하트 {status}"
                case "[일일 퀘스트] 기어드락 크로노스의 잔재 수집":
                    status = "✅" if content["quest_state"] == "2" else "❌"
                    # geardrak = f"기어드락 {status}"
                    quest = f"기어드락 {status}"

            daily_list.append(quest)
        embed.add_field(name="🗓️일일 퀘스트", value=" ".join(
            daily_list), inline=True)
    return embed


def get_weekly_content(response):
    character_name = response["character_name"]
    world_name = response["world_name"]
    character_level = response["character_level"]
    character_class = response["character_class"]

    embed = discord.Embed(
        title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)