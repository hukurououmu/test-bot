import sys
import discord
import wikipedia
from googlesearch import search


mode = 0
token = "1234567890" #自身のトークンを設置
client = discord.Client()


@client.event
async def on_ready():
    print("BOT Online")
    print("---------------")
    print("BOT_NAME:", client.user.name)
    print("BOT_ID  :", client.user.id)
    print("---------------")


@client.event
async def on_message(message):
    global mode
    msg = message.content

    if message.author.bot:
        return

    if msg == "!exit":
        await message.channel.send("終了します")
        sys.exit()

    if mode == 1:
        cnt = 0
        mode = 0
        for url in search(msg, lang="jp", num=5):
            await message.channel.send(url)
            cnt += 1
            if cnt == 5:
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

        await message.channel.send(wikipediaSearch(msg))
        mode = 0

    if msg == "!google":
        mode = 1
        await message.channel.send("検索ワードを発言してください")

    if msg == "!wiki":
        mode = 2
        await message.channel.send("調べたいワードを発言してください")


client.run(token)
