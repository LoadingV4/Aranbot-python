# from bot import bot
# from service.nexon import *
# from consts.colors import INFO_COLOR
# import discord
# import Paginator


# @bot.command(name="스케줄러", aliases=["스케쥴러", "할일", "스케줄"])
# async def scheduler(ctx, *, character_name: str):
#     ocid = get_ocid(character_name=character_name)
#     url = "https://open.api.nexon.com/maplestory/v1/scheduler/character-state?ocid="+ocid
#     embeds = generate_embed(send_request(url=url))

#     await Paginator.Simple().start(ctx=ctx, pages=embeds)


# def generate_embed(data):
#     weekly_bosses = get_weekly_boss(data=data)
#     daily_quests = get_daily_quests(data=data)
#     monster_park = get_monster_park(data=data)
#     weekly_contents = get_weekly_content(data=data)
#     return [weekly_bosses, daily_quests, weekly_contents, monster_park]


# def get_weekly_boss(data):
#     clear_count = data["weekly_boss_clear_count"]
#     limit_count = data["weekly_boss_clear_limit_count"]

#     character_name = data["character_name"]
#     world_name = data["world_name"]
#     character_level = data["character_level"]
#     character_class = data["character_class"]

#     embed = discord.Embed(
#         title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

#     weekly_bosses = [boss for boss in data["boss_contents"]
#                      if boss["registration_flag"] == "true" and boss["cycle"] == "bossWeekly"]

#     print(f"주간 보스({clear_count}/{limit_count}), {weekly_bosses}")

#     if not weekly_bosses:
#         embed.add_field(
#             name=f"😈주간 보스({clear_count}/{limit_count})", value="아직 보스를 돌지 않았거나 등록된 보스가 없습니다.❌")
#     # elif clear_count == limit_count:
#     #     embed.add_field(
#     #         name=f"😈주간 보스({clear_count}/{limit_count})", value=f"모두 클리어({clear_count}/{limit_count})✅")
#     else:
#         difficulty_map = {
#             "easy": "이지",
#             "normal": "노멀",
#             "hard": "하드",
#             "chaos": "카오스",
#             "extreme": "익스트림"
#         }

#         boss_list = {}
#         embed.add_field(
#             name=f"😈주간 보스({clear_count}/{limit_count})", value="", inline=False)
#         for boss in weekly_bosses:
#             name = boss["content_name"]

#             match name:
#                 case "선택받은 세렌":
#                     name = "세렌"
#                 case "감시자 칼로스":
#                     name = "칼로스"
#                 case "찬란한 흉성":
#                     name = "흉성"

#             difficulty = difficulty_map.get(
#                 boss["difficulty"], boss["difficulty"])

#             boss_name = f"{difficulty} {name}"

#             status = "✅" if boss["complete_flag"] == "true" else "❌"

#             boss_list[boss_name] = status
#             embed.add_field(
#                 name=boss_name, value=boss_list[boss_name], inline=True)

#     return embed


# def get_monster_park(data):
#     character_name = data["character_name"]
#     world_name = data["world_name"]
#     character_level = data["character_level"]
#     character_class = data["character_class"]

#     embed = discord.Embed(
#         title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

#     daily_contents = [content for content in data["daily_contents"]
#                       if content["registration_flag"] == "true"]
#     if daily_contents:
#         monster_park_flag = False
#         for content in daily_contents:
#             if content["content_name"] == "몬스터파크":
#                 monster_park_flag = True
#                 now_count = content["now_count"]
#                 max_count = content["max_count"]
#                 embed.add_field(
#                     name="몬파", value=f"몬파({now_count}/{max_count})", inline=False)
#         if monster_park_flag != True:
#             embed.add_field(
#                 name="몬파", value=f"스케쥴러에 몬파가 등록되지 않았습니다.❌", inline=False)
#     else:
#         embed.add_field(
#             name="몬파", value=f"스케쥴러에 몬파가 등록되지 않았습니다.❌", inline=False)
#     return embed


# def get_daily_quests(data):
#     character_name = data["character_name"]
#     world_name = data["world_name"]
#     character_level = data["character_level"]
#     character_class = data["character_class"]

#     embed = discord.Embed(
#         title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

#     daily_contents = [content for content in data["daily_contents"]
#                       if content["registration_flag"] == "true"]
#     if daily_contents:
#         daily_list = []
#         for content in daily_contents:
#             quest = ""

#             # yeoro = ""
#             # chuchu = ""
#             # lacheln = ""
#             # arcana = ""
#             # moras = ""
#             # esfera = ""
#             # moon_bridge = ""
#             # labyrinth = ""
#             # limen = ""

#             # cernium = ""
#             # hotel_arcs = ""
#             # audium = ""
#             # dowonkyung = ""
#             # arteria = ""
#             # carcion = ""
#             # tallahart = ""
#             # geardrak = ""

#             match content["content_name"]:
#                 case "[일일 퀘스트] 소멸의 여로 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # yeoro = f"여로 {status}"
#                     quest = f"여로 {status}"

#                 case "[일일 퀘스트] 츄츄 아일랜드 최고의 요리":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # chuchu = f"츄츄 {status}"
#                     quest = f"츄츄 {status}"

#                 case "[일일 퀘스트] 레헬른의 평온한 밤":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # lacheln = f"레헬른 {status}"
#                     quest = f"레헬른 {status}"

#                 case "[일일 퀘스트] 아르카나의 평온한 바람":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # arcana = f"아르카나 {status}"
#                     quest = f"아르카나 {status}"

#                 case "[일일 퀘스트] 모라스의 안정을 위해":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # moras = f"모라스 {status}"
#                     quest = f"모라스 {status}"

#                 case "[일일 퀘스트] 에스페라 연구 명령":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # esfera = f"에스페라 {status}"
#                     quest = f"에스페라 {status}"

#                 case "[일일 퀘스트] 문브릿지 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # moon_bridge = f"문브릿지 {status}"
#                     quest = f"문브릿지 {status}"

#                 case "[일일 퀘스트] 고통의 미궁 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # labyrinth = f"미궁 {status}"
#                     quest = f"미궁 {status}"

#                 case "[일일 퀘스트] 리멘 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # limen = f"리멘 {status}"
#                     quest = f"리멘 {status}"

#                 case "[일일 퀘스트] 세르니움 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # cernium = f"세르니움 {status}"
#                     quest = f"세르니움 {status}"

#                 case "[일일 퀘스트] 호텔 아르크스 주변 청소":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # hotel_arcs = f"호텔 아르크스 {status}"
#                     quest = f"호텔 아르크스 {status}"

#                 case "[일일 퀘스트] 오디움 일대 탐사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # audium = f"오디움 {status}"
#                     quest = f"오디움 {status}"

#                 case "[일일 퀘스트] 도원경 오염 정화":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # dowonkyung = f"도원경 {status}"
#                     quest = f"도원경 {status}"

#                 case "[일일 퀘스트] 아르테리아 잔당 처치":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # arteria = f"아르테리아 {status}"
#                     quest = f"아르테리아 {status}"

#                 case "[일일 퀘스트] 카르시온 복구 지원":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # carcion = f"카르시온 {status}"
#                     quest = f"카르시온 {status}"

#                 case "[일일 퀘스트] 탈라하트 고대신의 힘 조사":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # tallahart = f"탈라하트 {status}"
#                     quest = f"탈라하트 {status}"

#                 case "[일일 퀘스트] 기어드락 크로노스의 잔재 수집":
#                     status = "✅" if content["quest_state"] == "2" else "❌"
#                     # geardrak = f"기어드락 {status}"
#                     quest = f"기어드락 {status}"

#             daily_list.append(quest)
#         embed.add_field(name="🗓️일일 퀘스트", value=" ".join(
#             daily_list), inline=True)
#     return embed


# def get_weekly_content(data):
#     character_name = data["character_name"]
#     world_name = data["world_name"]
#     character_level = data["character_level"]
#     character_class = data["character_class"]

#     embed = discord.Embed(
#         title=f"{world_name} Lv.{character_level} {character_class} {character_name}의 스케쥴러", colour=INFO_COLOR)

#     weekly_contents = [content for content in data["weekly_contents"]
#                        if content["registration_flag"] == "true"]
#     if weekly_contents:
#         for content in weekly_contents:
#             content_name = content["content_name"]
#             get_epic_dungeon(embed, content, content_name)
#             get_union_coin(embed, content, content_name)
#             get_extreme_monster_park(embed, content, content_name)
#             get_arcane_weekly_quests(embed, content, content_name)
#             get_guild_contents(embed, content, content_name)
#         else:
#             embed.add_field(
#                 name="주간 컨텐츠", value="등록된 주간 컨텐츠가 없습니다.❌", inline=False)

#         return embed


# def get_guild_contents(embed, content, content_name):
#     match content_name:
#         case "[길드] 지하 수로":
#             now_count = content["now_count"]
#             embed.add_field(
#                 name="수로", value=f"{now_count}점" if now_count > 0 else "❌")
#         case "[길드] 플래그 레이스":
#             now_count = content["now_count"]
#             embed.add_field(
#                 name="플래그", value=f"{now_count}점" if now_count > 0 else "❌")


# def get_arcane_weekly_quests(embed, content, content_name):
#     match content_name:
#         case "에르다 스펙트럼":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(name="에르다 스펙트럼",
#                             value="✅" if quest_state else "❌", inline=False)
#         case "배고픈 무토":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(
#                 name="배고픈 무토", value="✅" if quest_state else "❌", inline=False)
#         case "미드나잇 체이서":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(name="미드나잇 체이서",
#                             value="✅" if quest_state else "❌", inline=False)
#         case "스피릿 세이비어":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(name="스피릿 세이비어",
#                             value="✅" if quest_state else "❌", inline=False)
#         case "엔하임 디펜스":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(
#                 name="엔하임 디펜스", value="✅" if quest_state else "❌", inline=False)
#         case "프로텍트 에스페라":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(name="프로텍트 에스페라",
#                             value="✅" if quest_state else "❌", inline=False)


# def get_extreme_monster_park(embed, content, content_name):
#     match content_name:
#         case "[몬스터파크] 익스트림 몬스터파커에 도전해보겠나?":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(
#                 name="익스트림 몬파", value="✅" if quest_state else "❌", inline=False)


# def get_union_coin(embed, content, content_name):
#     match content_name:
#         case "[메이플 유니온] 주간 드래곤 퇴치":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(
#                 name="🪙유니온 주간 코인", value="✅" if quest_state else "❌", inline=True)
#         case "[메이플 유니온] PC방 주간 드래곤 퇴치":
#             quest_state = content["quest_state"] == "2"
#             embed.add_field(
#                 name="🪙PC방 유니온 주간 코인", value="✅" if quest_state else "❌", inline=True)


# def get_epic_dungeon(embed, content, content_name):
#     match content_name:
#         case "에픽 던전 : 하이마운틴":
#             now_count = content["now_count"]
#             max_count = content["max_count"]
#             embed.add_field(
#                 name="🏔️에픽 던전 : 하이마운틴", value="✅" if now_count == 5 else f"❌ {now_count}/{max_count}")
#         case "에픽 던전 : 앵글러 컴퍼니":
#             now_count = content["now_count"]
#             max_count = content["max_count"]
#             embed.add_field(
#                 name="🪼에픽 던전 : 앵글러 컴퍼니", value="✅" if now_count == 5 else f"❌ {now_count}/{max_count}")
#         case "에픽 던전 : 앵글러 컴퍼니":
#             now_count = content["now_count"]
#             max_count = content["max_count"]
#             embed.add_field(
#                 name="🧠에픽 던전 : 악몽선경", value="✅" if now_count == 5 else f"❌ {now_count}/{max_count}")
#         case "에픽 던전 : 앵글러 컴퍼니":
#             now_count = content["now_count"]
#             max_count = content["max_count"]
#             embed.add_field(
#                 name="🕵️에픽 던전 : 아우룸 레기스", value="✅" if now_count == 5 else f"❌ {now_count}/{max_count}")
#         case _:
#             embed.add_field(
#                 name="에픽 던전", value="등록된 에픽 던전이 없습니다.❌", inline=False)
