import re
import sys
import json
import discord
import requests
import wikipedia
from googlesearch import search


token = "NTg2NTk2MTMwNDU3MTI0ODk0.XPqUhw.fMt9HzC2rVDz8j9akZ5_98KRg54"
client = discord.Client()
mode = 0
city_code = {
    "名古屋": "230010",
    "東京": "130010",
    "札幌": "016010",
    "横浜": "140010",
    "那覇": "471010",
    "大阪": "270000"
}


@client.event
async def on_ready():
    print("BOT Online")
    print("-"*28)
    print("BOT_NAME :", client.user.name)
    print("BOT_ID   :", client.user.id)
    print("-"*28)


@client.event
async def on_message(message):
    global mode
    global city_code
    msg = message.content

    if message.author.bot:
        return

    if msg == "!exit":
        await message.channel.send("終了しました")
        sys.exit()

    if msg == "!help":
        await message.channel.send("""
            Command Help
            \n!exit   : Botの活動を終了する
            \n!wiki   : 発言したワードをWikipediaで検索して表示する
            \n!google : 発言したワードをGoogle検索して10件表示する
            \n(city name)の天気は？ : その場所の3日間の天気予報を表示する"""
        )

    weathers = re.compile("(.+)の天気は？").search(message.content)
    if weathers:
        if weathers.group(1) in city_code.keys():
            city_code = city_code[weathers.group(1)]
            res = requests.get(
                "http://weather.livedoor.com/forecast/webservice/json/v1?city=%s" % city_code
            )
            res = json.loads(res.text.encode("utf-8"))

            weather_text = res["location"]["city"]
            weather_text += "の天気は、\n"
            for forecast in res["forecasts"]:
                weather_text += forecast["dateLabel"] + "が" + forecast["telop"] + "\n"
            weather_text += "です。"

            await message.channel.send(weather_text)
        else:
            await message.channel.send("そこの天気はわかりませんでした")

    if mode == 1:
        cnt = 0
        mode = 0
        await message.channel.send("{}で検索した結果です".format(msg))
        for url in search(msg, lang="jp", num=10):
            await message.channel.send(url)
            cnt += 1
            if cnt == 10:
                break

    if mode == 2:
        def wikipediaSearch(text):
            response_string = ""
            wikipedia.set_lang("ja")
            search_response = wikipedia.search(text)
            if not search_response:
                response_string = "見つかりませんでした"
                return response_string

            try:
                wiki_page = wikipedia.page(search_response[0])
            except:
                response_string = "エラーが発生しました"
                return response_string

            wiki_content = wiki_page.content
            response_string += wiki_content[0:200] + "......" + "\n"
            response_string += wiki_page.url

            return response_string

        await message.channel.send("{}で調べた結果です".format(msg))
        await message.channel.send(wikipediaSearch(msg))
        mode = 0

    if msg == "!google":
        mode = 1
        await message.channel.send("検索したいワードを発言してください")

    if msg == "!wiki":
        mode = 2
        await message.channel.send("調べたいワードを発言してください")


if __name__ == '__main__':
    client.run(token)
