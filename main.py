import asyncio
import os
from bot import bot
import listener.character_info
import listener.help
import listener.sunday

token = os.getenv('DISCORD_BOT_PYTHON_TOKEN')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


async def main():
    if token is None:
        print('토큰이 설정되지 않았습니다.')
        raise RuntimeError("토큰이 없습니다")
    print(bot.commands)
    await bot.start(token=token)

asyncio.run(main=main())
