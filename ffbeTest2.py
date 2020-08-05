import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import re
import os

async def handle(msg):
    global chat_id
    # These are some useful variables
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Log variables
    print(content_type, chat_type, chat_id)
    pprint(msg)
    username = msg['chat']['first_name']
    # Check that the content type is text and not the starting
    if content_type == 'text':
        text = msg['text']
        # it's better to strip and lower the input
        text = text.strip()
        if text.startswith('/'):
            if text == '/start':
                bienvenida = 'Hola querido!! a quien buscas? Dime parte del nombre, de la saga o se su combo y a ver que encuentro.\nTambién puedes usar los comandos para buscar por el rol que aparece en el juego, el rol que te mostraré yo es el definido por la comunidad'
                await bot.sendMessage(chat_id, bienvenida)
            else:
                roleUrl = 'https://www.ffbesearch.com/Characters?FilteringByRoles=True&star7=True&AllRoles=False' + text.replace("/","&") + '=True'
                await getUnitByRole(roleUrl)

        else:
            await getMeaning(text.lower())

        # https://www.ffbesearch.com/Characters?FilteringByRoles=True&star7=True&AllRoles=False&Breaker=False&Healer=False&MagicAttacker=False&MagicTank=False&PhysicalAttacker=True&PhysicalTank=False&Support=False&Versatile=False
        # https://www.ffbesearch.com/Characters?FilteringByRoles=True&star7=True&AllRoles=False&PhysicalAttacker=True


async def getMeaning(text):
    # create url
    # url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + text
    url = 'https://www.ffbesearch.com/Characters?'
    print(url)
    # get page
    page = requests.get(url)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # pprint(soup)
    resultNumber = 0
    try:
        try:
            # get definition
            # definition = soup.find('span', {'class': 'def'}).text
            # definition = soup.findAll('div', {'class': 'col-lg-3 col-md-6 col-sm-12 searchcard'})
            for definition in soup.findAll('div', {'class': 'card-header'}):
                # print(definition.text)
                myUnit = definition.text.lower()
                originalMyUnit = definition.text
                # print(text)
                # print(myUnit)
                if myUnit.find(text) >= 0:
                    # await bot.sendMessage(chat_id, definition.text)
                    # print(myUnit)
                    # await bot.sendMessage(chat_id, myUnit)
                    alt = definition.img['alt']
                    print(alt)
                    # await bot.sendMessage(chat_id, alt)
                    try:
                        lnk = 'https://www.ffbesearch.com/'+definition.img['data-src']
                    except:
                        lnk = 'https://www.ffbesearch.com/'+definition.img['src']
                    print(lnk)
                    # await bot.sendMessage(chat_id, lnk)
                    # await bot.sendPhoto(chat_id, lnk)
                    # await bot.send_photo(chat_id, photo=lnk)
                    rankUrl = 'https://www.ffbesearch.com/Rankings'
                    rankPage = requests.get(rankUrl)
                    # let's soup the page
                    rankSoup = BeautifulSoup(rankPage.text, 'html.parser')
                    try:
                        rankMyUnit = ''
                        for link in rankSoup.findAll('div', {'class': 'card-header'}):
                            rankMyUnit = link.text
                            # print(text)
                            # print(myUnit)
                            if rankMyUnit.find("\n"+alt+"\n") >= 0:
                                rankMyUnit = link.text
                                # print(rankMyUnit)
                                break
                            else: rankMyUnit = 'No hay información del ranking..'
                        originalMyUnit = originalMyUnit.replace("\r","")
                        originalMyUnit = originalMyUnit.replace("\n","")

                        rankMyUnit = rankMyUnit.replace("\r"," ")
                        rankMyUnit = rankMyUnit.replace("\n"," ")

                        originalMyUnit = originalMyUnit.replace(alt,"")                                
                        rankMyUnit = rankMyUnit.replace(alt,"")

                        originalMyUnit = originalMyUnit.replace("  "," ")                                
                        rankMyUnit = rankMyUnit.replace("  "," ")
                        originalMyUnit = originalMyUnit.strip()
                        rankMyUnit = rankMyUnit.strip()

                        info = alt + "\n" + originalMyUnit + "\n" + rankMyUnit

                                # await bot.sendMessage(chat_id, rankMyUnit)
                        if resultNumber < 10:
                            await bot.sendPhoto(chat_id, lnk, caption = info)
                            resultNumber = resultNumber +1
                        else:
                            await bot.sendMessage(chat_id, 'Hay más resultados pero estoy cansada...')
                            break

                    except:
                        await bot.sendMessage(chat_id, 'creo que no hay nada mas...')
            if resultNumber != 0:
                await bot.sendMessage(chat_id, 'eso es todo, puedo hacer algo mas por ti? ❤')
            else :
                await bot.sendMessage(chat_id, 'cariño... no he encontrado nada...')
        except:
            await bot.sendMessage(chat_id, 'Iba a decirte algo pero se me olvidó...')
    except:
        await bot.sendMessage(chat_id, 'Ahora mismo estoy ocupada...')

async def getUnitByRole(url):
    page = requests.get(url)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # pprint(soup)
    resultNumber = 0
    try:
        try:

            for definition in soup.findAll('div', {'class': 'card-header'}):
                # print(definition.text)
                myUnit = definition.text.lower()
                originalMyUnit = definition.text
                alt = definition.img['alt']
                print(alt)
                try:
                    lnk = 'https://www.ffbesearch.com/'+definition.img['data-src']
                except:
                    lnk = 'https://www.ffbesearch.com/'+definition.img['src']
                print(lnk)
                rankUrl = 'https://www.ffbesearch.com/Rankings'
                rankPage = requests.get(rankUrl)
                    # let's soup the page
                rankSoup = BeautifulSoup(rankPage.text, 'html.parser')
                try:
                    rankMyUnit = ''
                    for link in rankSoup.findAll('div', {'class': 'card-header'}):
                        rankMyUnit = link.text
                        # print(text)
                        # print(myUnit)
                        if rankMyUnit.find("\n"+alt+"\n") >= 0:
                            rankMyUnit = link.text
                            # print(rankMyUnit)
                            break
                        else: rankMyUnit = 'No hay información del ranking..'
                    originalMyUnit = originalMyUnit.replace("\r","")
                    originalMyUnit = originalMyUnit.replace("\n","")

                    rankMyUnit = rankMyUnit.replace("\r"," ")
                    rankMyUnit = rankMyUnit.replace("\n"," ")

                    originalMyUnit = originalMyUnit.replace(alt,"")                                
                    rankMyUnit = rankMyUnit.replace(alt,"")

                    originalMyUnit = originalMyUnit.replace("  "," ")                                
                    rankMyUnit = rankMyUnit.replace("  "," ")
                    originalMyUnit = originalMyUnit.strip()
                    rankMyUnit = rankMyUnit.strip()

                    info = alt + "\n" + originalMyUnit + "\n" + rankMyUnit
                    if resultNumber < 10:
                        await bot.sendPhoto(chat_id, lnk, caption = info)
                        resultNumber = resultNumber +1
                    else:
                        await bot.sendMessage(chat_id, 'Hay más resultados pero estoy cansada...')
                        break

                except:
                    await bot.sendMessage(chat_id, 'creo que no hay nada mas...')
            if resultNumber != 0:
                await bot.sendMessage(chat_id, 'eso es todo, puedo hacer algo mas por ti? ❤')
            else :
                await bot.sendMessage(chat_id, 'cariño... no he encontrado nada...')
        except:
            await bot.sendMessage(chat_id, 'Iba a decirte algo pero se me olvidó...')
    except:
        await bot.sendMessage(chat_id, 'Ahora mismo estoy ocupada...')

# Program startup
TOKEN = os.getenv("TOKEN")
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

# Keep the program running
loop.run_forever()