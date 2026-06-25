import discord
import json
from bot import bot
from service.nexon import *
from consts.colors import INFO_COLOR, ERROR_COLOR


@bot.command(name="썬데이", aliases=["선데이", "sunday", "sun"])
async def get_sunday_event(ctx):
    url = "https://open.api.nexon.com/maplestory/v1/notice-event"
    response = send_request(url)

    embed = discord.Embed()

    # 응답 자체가 비어있는 경우
    if not response:
        embed.color = ERROR_COLOR
        embed.title = ":no_entry: 에러"
        embed.add_field(
            name="넥슨에서 이벤트 정보를 가져오지 못했습니다.",
            value="```잠시 후 다시 시도해주세요.```",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    event_notice = response.get("event_notice")

    # 이벤트 목록 없음
    if not event_notice:
        embed.color = INFO_COLOR
        embed.title = ":information: 정보"
        embed.add_field(
            name="이벤트 정보가 없습니다.",
            value="```현재 진행중인 이벤트가 없습니다.```",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    sunday = get_sunday(event_notice)

    # 썬데이 메이플 없음
    if sunday is None:
        embed.color = INFO_COLOR
        embed.title = ":information: 정보"
        embed.add_field(
            name="썬데이 이벤트 공지가 없습니다.",
            value="```썬데이 메이플은 매주 금요일 오전 10시에 올라옵니다.```",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    notice_id = sunday["notice_id"]
    sunday_image_url = get_sunday_image_url(notice_id)

    embed.color = INFO_COLOR
    embed.title = ":sun: 이번주 썬데이는?"
    embed.set_image(url=sunday_image_url)

    embed.add_field(
        name=sunday["url"],
        value=":warning: 이미지를 클릭하면 크게 볼 수 있습니다. 잘 안 보인다면 링크를 이용해주세요.",
        inline=False
    )

    await ctx.send(embed=embed)


def get_sunday(event_notice):
    for notice in event_notice:
        if "썬데이 메이플" in notice.get("title", ""):
            print("썬데이 발견")
            return notice

    print("썬데이 없음")
    return None


def get_sunday_image_url(notice_id):
    url = (
        "https://open.api.nexon.com/maplestory/v1/"
        f"notice-event/detail?notice_id={notice_id}"
    )

    response = send_request(url)
    response_text = str(response)

    if ".jpg" in response_text:
        ext = ".jpg"
    else:
        ext = ".png"

    start = response_text.find("https://lwi.nexon.com")
    end = response_text.find(ext) + len(ext)

    return response_text[start:end]
