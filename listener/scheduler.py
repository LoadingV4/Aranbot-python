from bot import bot
from service.nexon import *
from consts.colors import INFO_COLOR, ERROR_COLOR
import discord


class SchedulerPaginationView(discord.ui.View):

    def __init__(
        self,
        pages: list[discord.Embed],
        author_id: int,
        timeout: float = 600.0
    ):
        super().__init__(timeout=timeout)

        self.pages = pages
        self.author_id = author_id
        self.current_page = 0

        # None만 대입하면 Pylance가 None 타입으로만 추론할 수 있으므로
        # discord.Message | None으로 명시합니다.
        self.message: discord.Message | None = None

        self.update_buttons()

    def update_buttons(self) -> None:
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = (
            self.current_page == len(self.pages) - 1
        )

        self.page_indicator.label = (
            f"{self.current_page + 1} / {len(self.pages)}"
        )

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "이 버튼은 명령어를 사용한 사람만 조작할 수 있습니다.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="이전",
        emoji="◀️",
        style=discord.ButtonStyle.secondary
    )
    async def previous_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        if self.current_page > 0:
            self.current_page -= 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.pages[self.current_page],
            view=self
        )

    @discord.ui.button(
        label="1 / 4",
        style=discord.ButtonStyle.secondary,
        disabled=True
    )
    async def page_indicator(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        pass

    @discord.ui.button(
        label="다음",
        emoji="▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ) -> None:
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.pages[self.current_page],
            view=self
        )

    async def on_timeout(self) -> None:
        """제한 시간이 지나면 버튼을 비활성화합니다."""

        # self.children은 Item 목록이므로 Button인지 확인해야 합니다.
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        # 지역 변수로 옮기면 타입 좁히기가 더욱 확실해집니다.
        message = self.message

        if message is None:
            return

        try:
            await message.edit(view=self)
        except discord.HTTPException:
            pass


@bot.command(name="스케줄러")
async def scheduler(ctx, *, character_name: str):
    scheduler_json = await get_scheduler(character_name=character_name)
    # print("스케줄러 : ",scheduler_json)
    # 캐릭터 정보
    world_name = scheduler_json["world_name"]
    # print(f"월드명 : {world_name}")
    character_level = scheduler_json["character_level"]
    character_class = scheduler_json["character_class"]

    daily_contents = scheduler_json["daily_contents"]
    # print("일일 : ", daily_contents)
    weekly_contents = scheduler_json["weekly_contents"]
    # print("주간 : ", weekly_contents)

    # 주간 컨텐츠
    monster_park = next(
        item for item in daily_contents if item["content_name"] == "몬스터파크")
    monster_park_now_count = monster_park["now_count"]
    monster_park_max_count = monster_park["max_count"]

    epic_dungeon_high_mountain = next(
        item for item in weekly_contents if item["content_name"] == "에픽 던전 : 하이마운틴")
    epic_dungeon_high_mountain_quest_state = epic_dungeon_high_mountain["quest_state"]

    epic_dungeon_angler_company = next(
        item for item in weekly_contents if item["content_name"] == "에픽 던전 : 앵글러 컴퍼니")
    epic_dungeon_angler_company_quest_state = epic_dungeon_angler_company["quest_state"]

    epic_dungeon_nightmare_paradise = next(
        item for item in weekly_contents if item["content_name"] == "에픽 던전 : 악몽선경")
    epic_dungeon_nightmare_paradise_quest_state = epic_dungeon_nightmare_paradise[
        "quest_state"]

    union_coin = next(
        item for item in weekly_contents if item["content_name"] == "[메이플 유니온] 주간 드래곤 퇴치")
    union_coin_quest_state = union_coin["quest_state"]

    extreme_monster_park = next(
        item for item in weekly_contents if item["content_name"] == "[몬스터파크] 익스트림 몬스터파커에 도전해보겠나?")
    extreme_monster_park_quest_state = extreme_monster_park["quest_state"]

    # 아케인리버 주간퀘
    erda_spectrum = next(
        item for item in weekly_contents if item["content_name"] == "에르다 스펙트럼")
    erda_spectrum_quest_state = erda_spectrum["quest_state"]

    hungry_muto = next(
        item for item in weekly_contents if item["content_name"] == "배고픈 무토")
    hungry_muto_quest_state = hungry_muto["quest_state"]

    midnight_chaser = next(
        item for item in weekly_contents if item["content_name"] == "미드나잇 체이서")
    midnight_chaser_quest_state = midnight_chaser["quest_state"]

    spirit_savior = next(
        item for item in weekly_contents if item["content_name"] == "스피릿 세이비어")
    spirit_savior_quest_state = spirit_savior["quest_state"]

    ranheim_defense = next(
        item for item in weekly_contents if item["content_name"] == "엔하임 디펜스")
    ranheim_defense_quest_state = ranheim_defense["quest_state"]

    protect_esfera = next(
        item for item in weekly_contents if item["content_name"] == "프로텍트 에스페라")
    protect_esfera_quest_state = protect_esfera["quest_state"]

    # 아케인리버 일퀘
    yeoro_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 소멸의 여로 조사")
    yeoro_daily_quest_complete_flag = yeoro_daily_quest["quest_state"]

    chuchu_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 츄츄 아일랜드 최고의 요리")
    chuchu_daily_quest_complete_flag = chuchu_daily_quest["quest_state"]

    lacheln_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 레헬른의 평온한 밤")
    lacheln_daily_quest_complete_flag = lacheln_daily_quest["quest_state"]

    arcana_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 아르카나의 평온한 바람")
    arcana_daily_quest_complete_flag = arcana_daily_quest["quest_state"]

    moras_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 모라스의 안정을 위해")
    moras_daily_quest_complete_flag = moras_daily_quest["quest_state"]

    esfera_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 에스페라 연구 명령")
    esfera_daily_quest_complete_flag = esfera_daily_quest["quest_state"]

    moonbridge_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 문브릿지 조사")
    moonbridge_daily_quest_complete_flag = moonbridge_daily_quest["quest_state"]

    labyrinth_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 고통의 미궁 조사")
    labyrinth_daily_quest_complete_flag = labyrinth_daily_quest["quest_state"]

    limen_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 리멘 조사")
    limen_daily_quest_complete_flag = limen_daily_quest["quest_state"]

    # 그란디스 일퀘
    cernium_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 세르니움 조사")
    cernium_daily_quest_complete_flag = cernium_daily_quest["quest_state"]

    hotel_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 호텔 아르크스 주변 청소")
    hotel_daily_quest_complete_flag = hotel_daily_quest["quest_state"]

    odium_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 오디움 일대 탐사")
    odium_daily_quest_complete_flag = odium_daily_quest["quest_state"]

    dowonkyung_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 도원경 오염 정화")
    dowonkyung_daily_quest_complete_flag = dowonkyung_daily_quest["quest_state"]

    arteria_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 아르테리아 잔당 처치")
    arteria_daily_quest_complete_flag = arteria_daily_quest["quest_state"]

    carcion_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 카르시온 복구 지원")
    carcion_daily_quest_complete_flag = carcion_daily_quest["quest_state"]

    talaheart_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 탈라하트 고대신의 힘 조사")
    talaheart_daily_quest_complete_flag = talaheart_daily_quest["quest_state"]

    geardrak_daily_quest = next(
        item for item in daily_contents if item["content_name"] == "[일일 퀘스트] 기어드락 크로노스의 잔재 수집")
    geardrak_daily_quest_complete_flag = geardrak_daily_quest["quest_state"]

    # 주간 보스
    boss_contents = scheduler_json["boss_contents"]

    # 자쿰
    zakum = next(
        item for item in boss_contents if item["content_name"] == "자쿰" and item["cycle"] == "bossWeekly")
    zakum_complete_flag = zakum["complete_flag"] == "true"

    # 매그너스
    magnus = next(
        item for item in boss_contents if item["content_name"] == "매그너스" and item["cycle"] == "bossWeekly")
    magnus_complete_flag = magnus["complete_flag"] == "true"

    # 파풀라투스
    papulatus = next(
        item for item in boss_contents if item["content_name"] == "파풀라투스" and item["cycle"] == "bossWeekly")
    papulatus_complete_flag = papulatus["complete_flag"] == "true"

    # 피에르
    pierre = next(
        item for item in boss_contents if item["content_name"] == "피에르" and item["cycle"] == "bossWeekly")
    pierre_complete_flag = pierre["complete_flag"] == "true"

    # 반반
    vonvon = next(
        item for item in boss_contents if item["content_name"] == "반반" and item["cycle"] == "bossWeekly")
    vonvon_complete_flag = vonvon["complete_flag"] == "true"

    # 블러디퀸
    queen = next(
        item for item in boss_contents if item["content_name"] == "블러디퀸" and item["cycle"] == "bossWeekly")
    queen_complete_flag = queen["complete_flag"] == "true"

    # 벨룸
    vellum = next(
        item for item in boss_contents if item["content_name"] == "벨룸" and item["cycle"] == "bossWeekly")
    vellum_complete_flag = vellum["complete_flag"] == "true"

    vellum = next(
        item for item in boss_contents if item["content_name"] == "벨룸" and item["cycle"] == "bossWeekly")
    vellum_complete_flag = vellum["complete_flag"] == "true"

    # 스우
    normal_siu = next(
        item for item in boss_contents if item["content_name"] == "스우" and item["difficulty"] == "normal")
    normal_siu_complete_flag = normal_siu["complete_flag"] == "true"

    hard_siu = next(
        item for item in boss_contents if item["content_name"] == "스우" and item["difficulty"] == "hard")
    hard_siu_complete_flag = hard_siu["complete_flag"] == "true"

    extreme_siu = next(
        item for item in boss_contents if item["content_name"] == "스우" and item["difficulty"] == "extreme")
    extreme_siu_complete_flag = extreme_siu["complete_flag"] == "true"

    # 데미안
    normal_demian = next(
        item for item in boss_contents if item["content_name"] == "데미안" and item["difficulty"] == "normal")
    normal_demian_complete_flag = normal_demian["complete_flag"] == "true"

    hard_demian = next(
        item for item in boss_contents if item["content_name"] == "데미안" and item["difficulty"] == "hard")
    hard_demian_complete_flag = hard_demian["complete_flag"] == "true"

    # 가디언 엔젤 슬라임(가엔슬)
    normal_slime = next(
        item for item in boss_contents if item["content_name"] == "가디언 엔젤 슬라임" and item["difficulty"] == "normal")
    normal_slime_complete_flag = normal_slime["complete_flag"] == "true"

    chaos_slime = next(
        item for item in boss_contents if item["content_name"] == "가디언 엔젤 슬라임" and item["difficulty"] == "chaos")
    chaos_slime_complete_flag = chaos_slime["complete_flag"] == "true"

    # 루시드
    easy_lucid = next(
        item for item in boss_contents if item["content_name"] == "루시드" and item["difficulty"] == "easy")
    easy_lucid_complete_flag = easy_lucid["complete_flag"] == "true"

    normal_lucid = next(
        item for item in boss_contents if item["content_name"] == "루시드" and item["difficulty"] == "normal")
    normal_lucid_complete_flag = normal_lucid["complete_flag"] == "true"

    hard_lucid = next(
        item for item in boss_contents if item["content_name"] == "루시드" and item["difficulty"] == "hard")
    hard_lucid_complete_flag = hard_lucid["complete_flag"] == "true"

    # 윌
    easy_will = next(
        item for item in boss_contents if item["content_name"] == "윌" and item["difficulty"] == "easy")
    easy_will_complete_flag = easy_will["complete_flag"] == "true"

    normal_will = next(
        item for item in boss_contents if item["content_name"] == "윌" and item["difficulty"] == "normal")
    normal_will_complete_flag = normal_will["complete_flag"] == "true"

    hard_will = next(
        item for item in boss_contents if item["content_name"] == "윌" and item["difficulty"] == "hard")
    hard_will_complete_flag = hard_will["complete_flag"] == "true"

    # 더스크
    normal_dusk = next(
        item for item in boss_contents if item["content_name"] == "더스크" and item["difficulty"] == "normal")
    normal_dusk_complete_flag = normal_dusk["complete_flag"] == "true"

    chaos_dusk = next(
        item for item in boss_contents if item["content_name"] == "더스크" and item["difficulty"] == "chaos")
    chaos_dusk_complete_flag = chaos_dusk["complete_flag"] == "true"

    # 진힐라
    normal_hilla = next(
        item for item in boss_contents if item["content_name"] == "진 힐라" and item["difficulty"] == "normal")
    normal_hilla_complete_flag = normal_hilla["complete_flag"] == "true"

    hard_hilla = next(
        item for item in boss_contents if item["content_name"] == "진 힐라" and item["difficulty"] == "hard")
    hard_hilla_complete_flag = hard_hilla["complete_flag"] == "true"

    # 듄켈
    normal_dunkel = next(
        item for item in boss_contents if item["content_name"] == "듄켈" and item["difficulty"] == "normal")
    normal_dunkel_complete_flag = normal_dunkel["complete_flag"] == "true"

    hard_dunkel = next(
        item for item in boss_contents if item["content_name"] == "듄켈" and item["difficulty"] == "hard")
    hard_dunkel_complete_flag = hard_dunkel["complete_flag"] == "true"

    # 세렌
    normal_seren = next(
        item for item in boss_contents if item["content_name"] == "선택받은 세렌" and item["difficulty"] == "normal")
    normal_seren_complete_flag = normal_seren["complete_flag"] == "true"

    hard_seren = next(
        item for item in boss_contents if item["content_name"] == "선택받은 세렌" and item["difficulty"] == "hard")
    hard_seren_complete_flag = hard_seren["complete_flag"] == "true"

    extreme_seren = next(
        item for item in boss_contents if item["content_name"] == "선택받은 세렌" and item["difficulty"] == "extreme")
    extreme_seren_complete_flag = extreme_seren["complete_flag"] == "true"

    # 칼로스
    easy_kalos = next(
        item for item in boss_contents if item["content_name"] == "감시자 칼로스" and item["difficulty"] == "easy")
    easy_kalos_complete_flag = easy_kalos["complete_flag"] == "true"

    normal_kalos = next(
        item for item in boss_contents if item["content_name"] == "감시자 칼로스" and item["difficulty"] == "normal")
    normal_kalos_complete_flag = normal_kalos["complete_flag"] == "true"

    chaos_kalos = next(
        item for item in boss_contents if item["content_name"] == "감시자 칼로스" and item["difficulty"] == "chaos")
    chaos_kalos_complete_flag = chaos_kalos["complete_flag"] == "true"

    extreme_kalos = next(
        item for item in boss_contents if item["content_name"] == "감시자 칼로스" and item["difficulty"] == "extreme")
    extreme_kalos_complete_flag = extreme_kalos["complete_flag"] == "true"

    # 카링
    easy_carling = next(
        item for item in boss_contents if item["content_name"] == "카링" and item["difficulty"] == "easy")
    easy_carling_complete_flag = easy_carling["complete_flag"] == "true"

    normal_carling = next(
        item for item in boss_contents if item["content_name"] == "카링" and item["difficulty"] == "normal")
    normal_carling_complete_flag = normal_carling["complete_flag"] == "true"

    hard_carling = next(
        item for item in boss_contents if item["content_name"] == "카링" and item["difficulty"] == "hard")
    hard_carling_complete_flag = hard_carling["complete_flag"] == "true"

    extreme_carling = next(
        item for item in boss_contents if item["content_name"] == "카링" and item["difficulty"] == "extreme")
    extreme_carling_complete_flag = extreme_carling["complete_flag"] == "true"

    # 림보
    normal_limbo = next(
        item for item in boss_contents if item["content_name"] == "림보" and item["difficulty"] == "normal")
    normal_limbo_complete_flag = normal_limbo["complete_flag"] == "true"

    hard_limbo = next(
        item for item in boss_contents if item["content_name"] == "림보" and item["difficulty"] == "hard")
    hard_limbo_complete_flag = hard_limbo["complete_flag"] == "true"

    # 발드릭스
    normal_baldrix = next(
        item for item in boss_contents if item["content_name"] == "발드릭스" and item["difficulty"] == "normal")
    normal_baldrix_complete_flag = normal_baldrix["complete_flag"] == "true"

    hard_baldrix = next(
        item for item in boss_contents if item["content_name"] == "발드릭스" and item["difficulty"] == "hard")
    hard_baldrix_complete_flag = hard_baldrix["complete_flag"] == "true"

    # 최초의 대적자
    easy_first_adversary = next(
        item for item in boss_contents if item["content_name"] == "최초의 대적자" and item["difficulty"] == "easy")
    easy_first_adversary_complete_flag = easy_first_adversary["complete_flag"] == "true"

    normal_first_adversary = next(
        item for item in boss_contents if item["content_name"] == "최초의 대적자" and item["difficulty"] == "normal")
    normal_first_adversary_complete_flag = normal_first_adversary["complete_flag"] == "true"

    hard_first_adversary = next(
        item for item in boss_contents if item["content_name"] == "최초의 대적자" and item["difficulty"] == "hard")
    hard_first_adversary_complete_flag = hard_first_adversary["complete_flag"] == "true"

    extreme_first_adversary = next(
        item for item in boss_contents if item["content_name"] == "최초의 대적자" and item["difficulty"] == "extreme")
    extreme_first_adversary_complete_flag = extreme_first_adversary["complete_flag"] == "true"

    # 찬란한 흉성
    normal_malefic_star = next(
        item for item in boss_contents if item["content_name"] == "찬란한 흉성" and item["difficulty"] == "normal")
    normal_malefic_star_complete_flag = normal_malefic_star["complete_flag"] == "true"

    hard_malefic_star = next(
        item for item in boss_contents if item["content_name"] == "찬란한 흉성" and item["difficulty"] == "hard")
    hard_malefic_star_complete_flag = hard_malefic_star["complete_flag"] == "true"

    # 유피테르
    normal_jupiter = next(
        item for item in boss_contents if item["content_name"] == "유피테르" and item["difficulty"] == "normal")
    normal_jupiter_complete_flag = normal_jupiter["complete_flag"] == "true"

    hard_jupiter = next(
        item for item in boss_contents if item["content_name"] == "유피테르" and item["difficulty"] == "hard")
    hard_jupiter_complete_flag = hard_jupiter["complete_flag"] == "true"

    # 시즌 보스
    normal_maerin = next(
        item for item in boss_contents if item["content_name"] == "시즌 보스 메이린" and item["difficulty"] == "normal")
    normal_normal_maerin_complete_flag = normal_maerin["complete_flag"] == "true"

    hard_maerin = next(
        item for item in boss_contents if item["content_name"] == "시즌 보스 메이린" and item["difficulty"] == "hard")
    hard_maerin_complete_flag = hard_maerin["complete_flag"] == "true"

    # 주간 보스 제한
    weekly_boss_clear_count = scheduler_json["weekly_boss_clear_count"]
    weekly_boss_clear_limit_count = scheduler_json["weekly_boss_clear_limit_count"]

    # 월간 보스
    hard_black_mage = next(
        item for item in boss_contents if item["content_name"] == "검은 마법사" and item["difficulty"] == "hard")
    hard_black_mage_complete_flag = hard_black_mage["complete_flag"] == "true"

    extreme_black_mage = next(
        item for item in boss_contents if item["content_name"] == "검은 마법사" and item["difficulty"] == "extreme")
    extreme_black_mage_complete_flag = extreme_black_mage["complete_flag"] == "true"

    # 임베드 공통 제목
    base_title = (
        f"{world_name}의 Lv.{character_level} "
        f"{character_name}({character_class}) 스케줄 현황"
    )

    CHECK = ":white_check_mark:"
    CROSS = ":x:"


    # =========================================================
    # 1페이지: 주간 보스 + 월간 보스
    # =========================================================

    embed1 = discord.Embed(
        title=f"{base_title} (1/4)",
        description=(
            f"**주간 보스**\n"
            f"주간 보스 클리어 횟수: "
            f"`{weekly_boss_clear_count}/{weekly_boss_clear_limit_count}`"
        ),
        color=INFO_COLOR
    )

    embed1.add_field(
        name="자쿰",
        value=CHECK if zakum_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="매그너스",
        value=CHECK if magnus_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="파풀라투스",
        value=CHECK if papulatus_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="피에르",
        value=CHECK if pierre_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="반반",
        value=CHECK if vonvon_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="블러디퀸",
        value=CHECK if queen_complete_flag else CROSS,
        inline=True
    )
    embed1.add_field(
        name="벨룸",
        value=CHECK if vellum_complete_flag else CROSS,
        inline=True
    )


    # 스우
    if extreme_siu_complete_flag:
        embed1.add_field(
            name="스우(익스트림)",
            value=CHECK,
            inline=True
        )
    elif hard_siu_complete_flag:
        embed1.add_field(
            name="스우(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_siu_complete_flag:
        embed1.add_field(
            name="스우(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="스우",
            value=CROSS,
            inline=True
        )


    # 데미안
    if hard_demian_complete_flag:
        embed1.add_field(
            name="데미안(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_demian_complete_flag:
        embed1.add_field(
            name="데미안(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="데미안",
            value=CROSS,
            inline=True
        )


    # 가디언 엔젤 슬라임
    if chaos_slime_complete_flag:
        embed1.add_field(
            name="가엔슬(카오스)",
            value=CHECK,
            inline=True
        )
    elif normal_slime_complete_flag:
        embed1.add_field(
            name="가엔슬(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="가엔슬",
            value=CROSS,
            inline=True
        )


    # 루시드
    if hard_lucid_complete_flag:
        embed1.add_field(
            name="루시드(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_lucid_complete_flag:
        embed1.add_field(
            name="루시드(노말)",
            value=CHECK,
            inline=True
        )
    elif easy_lucid_complete_flag:
        embed1.add_field(
            name="루시드(이지)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="루시드",
            value=CROSS,
            inline=True
        )


    # 윌
    if hard_will_complete_flag:
        embed1.add_field(
            name="윌(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_will_complete_flag:
        embed1.add_field(
            name="윌(노말)",
            value=CHECK,
            inline=True
        )
    elif easy_will_complete_flag:
        embed1.add_field(
            name="윌(이지)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="윌",
            value=CROSS,
            inline=True
        )


    # 더스크
    if chaos_dusk_complete_flag:
        embed1.add_field(
            name="더스크(카오스)",
            value=CHECK,
            inline=True
        )
    elif normal_dusk_complete_flag:
        embed1.add_field(
            name="더스크(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="더스크",
            value=CROSS,
            inline=True
        )


    # 진 힐라
    if hard_hilla_complete_flag:
        embed1.add_field(
            name="진 힐라(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_hilla_complete_flag:
        embed1.add_field(
            name="진 힐라(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="진 힐라",
            value=CROSS,
            inline=True
        )


    # 듄켈
    if hard_dunkel_complete_flag:
        embed1.add_field(
            name="듄켈(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_dunkel_complete_flag:
        embed1.add_field(
            name="듄켈(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="듄켈",
            value=CROSS,
            inline=True
        )


    # 세렌
    if extreme_seren_complete_flag:
        embed1.add_field(
            name="세렌(익스트림)",
            value=CHECK,
            inline=True
        )
    elif hard_seren_complete_flag:
        embed1.add_field(
            name="세렌(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_seren_complete_flag:
        embed1.add_field(
            name="세렌(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="세렌",
            value=CROSS,
            inline=True
        )


    # 칼로스
    if extreme_kalos_complete_flag:
        embed1.add_field(
            name="칼로스(익스트림)",
            value=CHECK,
            inline=True
        )
    elif chaos_kalos_complete_flag:
        embed1.add_field(
            name="칼로스(카오스)",
            value=CHECK,
            inline=True
        )
    elif normal_kalos_complete_flag:
        embed1.add_field(
            name="칼로스(노말)",
            value=CHECK,
            inline=True
        )
    elif easy_kalos_complete_flag:
        embed1.add_field(
            name="칼로스(이지)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="칼로스",
            value=CROSS,
            inline=True
        )


    # 카링
    if extreme_carling_complete_flag:
        embed1.add_field(
            name="카링(익스트림)",
            value=CHECK,
            inline=True
        )
    elif hard_carling_complete_flag:
        embed1.add_field(
            name="카링(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_carling_complete_flag:
        embed1.add_field(
            name="카링(노말)",
            value=CHECK,
            inline=True
        )
    elif easy_carling_complete_flag:
        embed1.add_field(
            name="카링(이지)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="카링",
            value=CROSS,
            inline=True
        )


    # 림보
    if hard_limbo_complete_flag:
        embed1.add_field(
            name="림보(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_limbo_complete_flag:
        embed1.add_field(
            name="림보(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="림보",
            value=CROSS,
            inline=True
        )


    # 발드릭스
    if hard_baldrix_complete_flag:
        embed1.add_field(
            name="발드릭스(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_baldrix_complete_flag:
        embed1.add_field(
            name="발드릭스(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="발드릭스",
            value=CROSS,
            inline=True
        )


    # 최초의 대적자
    if extreme_first_adversary_complete_flag:
        embed1.add_field(
            name="최초의 대적자(익스트림)",
            value=CHECK,
            inline=True
        )
    elif hard_first_adversary_complete_flag:
        embed1.add_field(
            name="최초의 대적자(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_first_adversary_complete_flag:
        embed1.add_field(
            name="최초의 대적자(노말)",
            value=CHECK,
            inline=True
        )
    elif easy_first_adversary_complete_flag:
        embed1.add_field(
            name="최초의 대적자(이지)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="최초의 대적자",
            value=CROSS,
            inline=True
        )


    # 찬란한 흉성
    if hard_malefic_star_complete_flag:
        embed1.add_field(
            name="찬란한 흉성(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_malefic_star_complete_flag:
        embed1.add_field(
            name="찬란한 흉성(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="찬란한 흉성",
            value=CROSS,
            inline=True
        )


    # 유피테르
    if hard_jupiter_complete_flag:
        embed1.add_field(
            name="유피테르(하드)",
            value=CHECK,
            inline=True
        )
    elif normal_jupiter_complete_flag:
        embed1.add_field(
            name="유피테르(노말)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="유피테르",
            value=CROSS,
            inline=True
        )


    # 월간 보스
    embed1.add_field(
        name="\u200b",
        value="월간 보스",
        inline=False
    )

    if extreme_black_mage_complete_flag:
        embed1.add_field(
            name="검은 마법사(익스트림)",
            value=CHECK,
            inline=True
        )
    elif hard_black_mage_complete_flag:
        embed1.add_field(
            name="검은 마법사(하드)",
            value=CHECK,
            inline=True
        )
    else:
        embed1.add_field(
            name="검은 마법사",
            value=CROSS,
            inline=True
        )


    # =========================================================
    # 2페이지: 몬스터파크 + 그란디스 일일 퀘스트
    # =========================================================

    embed2 = discord.Embed(
        title=f"{base_title} (2/4)",
        description="**몬스터파크 · 그란디스 일일 퀘스트**",
        color=INFO_COLOR
    )

    embed2.add_field(
        name="몬스터파크",
        value=f"`{monster_park_now_count}/{monster_park_max_count}`",
        inline=False
    )

    embed2.add_field(
        name="세르니움",
        value=CHECK if cernium_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="호텔 아르크스",
        value=CHECK if hotel_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="오디움",
        value=CHECK if odium_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="도원경",
        value=CHECK if dowonkyung_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="아르테리아",
        value=CHECK if arteria_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="카르시온",
        value=CHECK if carcion_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="탈라하트",
        value=CHECK if talaheart_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed2.add_field(
        name="기어드락",
        value=CHECK if geardrak_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )


    # =========================================================
    # 3페이지: 주간 컨텐츠
    # =========================================================

    embed3 = discord.Embed(
        title=f"{base_title} (3/4)",
        description="**주간 컨텐츠**",
        color=INFO_COLOR
    )

    embed3.add_field(
        name="에픽 던전",
        value="\u200b",
        inline=False
    )
    embed3.add_field(
        name="하이마운틴",
        value=(
            CHECK
            if epic_dungeon_high_mountain_quest_state == "2"
            else CROSS
        ),
        inline=True
    )
    embed3.add_field(
        name="앵글러 컴퍼니",
        value=(
            CHECK
            if epic_dungeon_angler_company_quest_state == "2"
            else CROSS
        ),
        inline=True
    )
    embed3.add_field(
        name="악몽선경",
        value=(
            CHECK
            if epic_dungeon_nightmare_paradise_quest_state == "2"
            else CROSS
        ),
        inline=True
    )

    embed3.add_field(
        name="익스트림 몬스터파크",
        value=CHECK if extreme_monster_park_quest_state == "2" else CROSS,
        inline=True
    )

    embed3.add_field(
        name="메이플 유니온 주간 드래곤 퇴치",
        value=CHECK if union_coin_quest_state == "2" else CROSS,
        inline=True
    )


    # =========================================================
    # 4페이지: 아케인리버 일일 + 주간 컨텐츠
    # =========================================================

    embed4 = discord.Embed(
        title=f"{base_title} (4/4)",
        description="**아케인리버 일일 퀘스트 · 주간 컨텐츠**",
        color=INFO_COLOR
    )

    embed4.add_field(
        name="아케인리버 일일 퀘스트",
        value="\u200b",
        inline=False
    )

    embed4.add_field(
        name="소멸의 여로",
        value=CHECK if yeoro_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="츄츄 아일랜드",
        value=CHECK if chuchu_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="꿈의 도시 레헬른",
        value=CHECK if lacheln_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="신비의 숲 아르카나",
        value=CHECK if arcana_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="기억의 늪 모라스",
        value=CHECK if moras_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="태초의 바다 에스페라",
        value=CHECK if esfera_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="문브릿지",
        value=CHECK if moonbridge_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="고통의 미궁",
        value=CHECK if labyrinth_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="리멘",
        value=CHECK if limen_daily_quest_complete_flag == "2" else CROSS,
        inline=True
    )

    embed4.add_field(
        name="아케인리버 주간 컨텐츠",
        value="\u200b",
        inline=False
    )

    embed4.add_field(
        name="에르다 스펙트럼",
        value=CHECK if erda_spectrum_quest_state == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="배고픈 무토",
        value=CHECK if hungry_muto_quest_state == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="미드나잇 체이서",
        value=CHECK if midnight_chaser_quest_state == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="스피릿 세이비어",
        value=CHECK if spirit_savior_quest_state == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="엔하임 디펜스",
        value=CHECK if ranheim_defense_quest_state == "2" else CROSS,
        inline=True
    )
    embed4.add_field(
        name="프로텍트 에스페라",
        value=CHECK if protect_esfera_quest_state == "2" else CROSS,
        inline=True
    )


    pages = [
        embed1,  # 1페이지: 주간 보스 + 월간 보스
        embed2,  # 2페이지: 몬스터파크 + 그란디스 일일 퀘스트
        embed3,  # 3페이지: 주간 컨텐츠
        embed4   # 4페이지: 아케인리버 일일 + 주간 컨텐츠
    ]

    view = SchedulerPaginationView(
        pages=pages,
        author_id=ctx.author.id,
        timeout=180.0
    )

    message = await ctx.reply(
        embed=pages[0],
        view=view
    )

    # timeout 발생 시 버튼을 비활성화하기 위해 메시지를 저장합니다.
    view.message = message


def get_ocid(character_name: str) -> str:
    url = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + character_name
    response = send_request(url)
    if response:
        return response.get("ocid")
    else:
        return response.get("error")


async def get_scheduler(character_name):
    ocid = get_ocid(character_name=character_name)
    url = "https://open.api.nexon.com/maplestory/v1/scheduler/character-state?ocid=" + ocid
    response = send_request(url=url)
    return response
