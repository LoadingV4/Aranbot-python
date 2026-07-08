import urllib.parse
import discord
from bot import bot

from consts.colors import INFO_COLOR, ERROR_COLOR
from service.nexon import send_request

WORLDS = [
    "스카니아",
    "베라",
    "루나",
    "제니스",
    "크로아",
    "유니온",
    "엘리시움",
    "이노시스",
    "레드",
    "오로라",
    "아케인",
    "노바",
    "챌린저스1",
    "챌린저스2",
    "챌린저스3",
    "챌린저스4",
]

def check_guild_name(guild_name):
    hangul = 0
    english = 0
    num = 0
    nickname_minimum = 2
    nickname_limit = 6

    for c in guild_name:
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

@bot.command(name="길드", aliases=["guild"])
async def guild(ctx, *, guild_name: str):
    if not check_guild_name(guild_name=guild_name):
        embed = discord.Embed(
            title=":no_entry: **유효하지 않은 길드명입니다.**", color=ERROR_COLOR)
        embed.add_field(name="다른 길드명을 시도해주세요.",
                        value=f"```입력한 길드명 : {guild_name}\n\n1. 길드명은 6글자 제한입니다.(영문과 숫자는 한 글자당 0.5글자)\n2. 특수문자 또는 한글 모음, 자음 단독으로는 사용할 수 없습니다.\n3. 공백은 사용 불가합니다.```", inline=False)
        await ctx.reply(embed=embed)
        return
    
    view = WorldView(guild_name, ctx.author)

    await ctx.reply(
        "월드를 선택해주세요.",
        view=view
    )


class WorldView(discord.ui.View):
    def __init__(self, guild_name: str, author: discord.Member):
        super().__init__(timeout=60)

        self.author = author
        self.add_item(WorldSelect(guild_name))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "명령어를 입력한 사람만 사용할 수 있습니다.",
                ephemeral=True
            )
            return False

        return True


class WorldSelect(discord.ui.Select):
    def __init__(self, guild_name: str):
        self.guild_name = guild_name

        options = [
            discord.SelectOption(label=world)
            for world in WORLDS
        ]

        super().__init__(
            placeholder="월드를 선택하세요.",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        world = self.values[0]

        embed = get_guild_embed(self.guild_name, world)

        await interaction.response.edit_message(
            content=f"**{world}**  **{self.guild_name}**",
            embed=embed,
            view=None
        )


def get_guild_embed(guild_name: str, world: str):
    url = get_oguild_id_request_url(guild_name, world)
    response = send_request(url)

    oguild_id = response.get("oguild_id")

    if oguild_id is None:
        embed = discord.Embed(
            title=":no_entry: **에러**",
            color=ERROR_COLOR
        )
        embed.add_field(
            name="길드 정보를 불러오는데 실패했습니다.",
            value="```존재하지 않는 길드입니다.\n길드명이나 월드를 확인해주세요.```",
            inline=False
        )
        return embed

    response = send_request(
        f"https://open.api.nexon.com/maplestory/v1/guild/basic?oguild_id={oguild_id}"
    )

    noblesse_skills = response.get("guild_noblesse_skill", [])

    boss_skill = "보스 킬링 머신"
    ignore_guard_skill = "방어력은 숫자일 뿐"
    critical_damage_skill = "크게 한방"
    damage_skill = "길드의 이름으로"

    world_name = response.get("world_name")
    received_guild_name = response.get("guild_name")
    guild_master_name = response.get("guild_master_name")

    guild_member_count = response.get("guild_member_count")
    guild_level = response.get("guild_level")

    # is_full_level = guild_level == 30

    embed = discord.Embed(
        title=f"Lv.{guild_level} {received_guild_name}",
        color=INFO_COLOR
    )

    # embed.add_field(
    #     name="만렙 여부",
    #     value=":white_check_mark:" if is_full_level else ":x:",
    #     inline=False
    # )

    embed.add_field(
        name="길드명",
        value=received_guild_name,
        inline=False
    )

    embed.add_field(
        name="월드",
        value=world_name,
        inline=False
    )

    embed.add_field(
        name="길드마스터",
        value=guild_master_name,
        inline=False
    )

    embed.add_field(
        name="인원수",
        value=str(guild_member_count),
        inline=False
    )

    if noblesse_skills:
        boss_level = get_skill_level(
            noblesse_skills,
            boss_skill
        )

        ignore_guard_level = get_skill_level(
            noblesse_skills,
            ignore_guard_skill
        )

        damage_level = get_skill_level(
            noblesse_skills,
            damage_skill
        )

        critical_damage_level = get_skill_level(
            noblesse_skills,
            critical_damage_skill
        )

        total_point = (
            boss_level
            + ignore_guard_level
            + damage_level
            + critical_damage_level
        )

        embed.add_field(
            name="총합 노블 포인트",
            value=str(total_point),
            inline=False
        )

        embed.add_field(
            name="노블스킬",
            value=(
                "```"
                f"1. {boss_skill}\n"
                f"Lv.{boss_level}\n\n"

                f"2. {ignore_guard_skill}\n"
                f"Lv.{ignore_guard_level}\n\n"

                f"3. {damage_skill}\n"
                f"Lv.{damage_level}\n\n"

                f"4. {critical_damage_skill}\n"
                f"Lv.{critical_damage_level}"
                "```"
            ),
            inline=False
        )

    else:
        embed.add_field(
            name="노블스킬",
            value="노블스킬이 없는 길드입니다. :x:",
            inline=False
        )

    return embed


def get_oguild_id_request_url(guild_name: str, world: str):
    guild_name = urllib.parse.quote(guild_name)
    world = urllib.parse.quote(world)

    return (
        "https://open.api.nexon.com/maplestory/v1/guild/id?"
        f"guild_name={guild_name}&world_name={world}"
    )


def get_skill_level(noblesse_skills: list, skill_name: str):
    for skill in noblesse_skills:
        if skill.get("skill_name") == skill_name:
            return skill.get("skill_level", 0)

    return 0