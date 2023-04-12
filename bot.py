import loader
import discord
import crawler
from time import sleep, strftime

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    # 봇 상태 정의
    game = discord.Game('크롤링')
    await bot.change_presence(activity=game, status=discord.Status.online)

    # 봇 구동 시 메시지 전송
    notice_channel = bot.get_channel(int(loader.get_env('notice_channel_id')))
    await notice_channel.send(f'Server start!\n{get_date_time()}')

    # 봇 정보
    print(f'login sucess: {bot.user}')
    print(f'id is \"{bot.user.id}\"')

    # 크롤링 전 로그인
    driver = crawler.create_driver()
    crawler.login(driver)

    # 크롤링 시작
    now_number = '0'
    alimi_channel = bot.get_channel(int(loader.get_env('alimi_channel_id')))
    try:
        while True:
            result = crawler.start(driver)
            if result['number'] != now_number:
                now_number = result['number']
                message = mapping(result)
                await alimi_channel.send(message)
            sleep(5)
    except KeyboardInterrupt as e:
        await notice_channel.send(f'Server terminated.\n{get_date_time()}')
        exit()
    except RuntimeError as e:
        await notice_channel.send(f'runtime error occured.\n\
                                  Server closed.\n{get_date_time()}')


def mapping(crawl_result: dict):
    message = '---------------------------------------\n'
    for key, value in crawl_result.items():
        if key == 'number':
            continue
        message += f'{key}: {value}\n'
    message += '---------------------------------------'
    return message


def get_date_time():
    return f'Date: {strftime("%Y.%m.%d (%a)")}\nTime: {strftime("%X")}'


if __name__ == '__main__':
    bot.run(loader.get_env('discord_token'))
