from typing import Any, Union

5# <editor-fold desc="Important Stuff to not look at">
import asyncio
import r6sapi as api
import requests
from time import sleep
import json

auth = api.Auth("Leonard.r.wecke@gmail.com", "Tachch3n")
token = '585021350:AAEciXskrmka0wp1xejUsi792YFLiTcg_xY'
url = 'https://api.telegram.org/bot{}/'.format(token)
SLEEP_TIME = 0.5
playerButtons=['Remove Player','Add Player','Ng-Bullseye','Ng-Ironman','Ng-Loki','Ng-Brofessionel','Ng-Groot','Ng-Nemo']
playerSkillButtons=[]
SkillButtons=[]
reply_markup=None
def get_updates(offset=None):
    while True:
        try:
            URL = url + 'getUpdates'
            if offset:
                URL += '?offset={}'.format(offset)

            res = requests.get(URL)
            while (res.status_code != 200 or len(res.json()['result']) == 0):
                asyncio.sleep(1)
                res = requests.get(URL)
            print(res.url)
            return res.json()

        except:
            pass;


def get_last(data):
    results = data['result']
    count = len(results)
    last = count - 1
    last_update = results[last]
    return last_update


def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id = last_update['message']['chat']['id']
    update_id = last_update['update_id']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id, text, update_id


def send_message(chat_id, text, reply_markup=None):
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)
    while res.status_code != 200:
        res = requests.get(URL)
    print(res.status_code)


def reply_markup_maker(data):
    keyboard = []
    for i in range(0, len(data), 2):
        key = []
        key.append(data[i].title())
        try:
            key.append(data[i + 1].title())
        except:
            pass
        keyboard.append(key)

    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


# </editor-fold>

def playerButtonAdding(tag):
    i=0
    while i<len(playerButtons):
        if tag in playerButtons[i]:
            return tag
        i=i+1
    playerButtons.append(tag)
    return tag

def getMMR(tag,update_id):
    global auth
    try:
        player = yield from auth.get_player(tag, api.Platforms.UPLAY)
    except:
        chat_id, text, update_id = get_last_id_text(get_updates(update_id))
        send_message(chat_id, "No player found")
        return 0, update_id
    try:
        rank = yield from player.get_rank("emea")
        chat_id, text, update_id = get_last_id_text(get_updates(update_id))
        skill =rank.skill_mean
        print(skill)
        return skill, update_id
    except:
        chat_id, text, update_id = get_last_id_text(get_updates(update_id))
        send_message(chat_id, "Cant fetch the Rank from the Ubisoft Servers")
        return 0, update_id

def updateMMR(update_id):
    i=0
    sleep(SLEEP_TIME)

    while i<len(playerButtons):
        if i>2:
            sleep(SLEEP_TIME)
            skill,update_id=getMMR(playerButtons[i],update_id)
            playerSkillButtons[i]=playerButtons[i]+" "+str(skill)
        i=i+1
    return reply_markup_maker(playerSkillButtons),update_id



def checkForModes(tag,chat_id,update_id):
    global reply_markup
    if 'Remove Player' in tag:
        reply_markup = reply_markup_maker(playerButtons)
        text = "Choose Name to remove"
        send_message(chat_id, text,reply_markup)
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        if text in playerButtons:
            playerButtons.remove(text)
        else:
            send_message(chat_id, "Not found")
        return tag

    if 'Add Player' in tag:
        text = "Enter Name to add"
        send_message(chat_id, text)
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        if text not in playerButtons:
            playerButtons.append(text)
        else:
            chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
            send_message(chat_id, "already in there")
        return text

    if 'Refresh' in tag:
        text = "Refreshing"
        sleep(SLEEP_TIME)
       #chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        reply_markup,update_id=updateMMR(update_id)
        send_message(chat_id, text,reply_markup)
    return tag

def playerInfo():
    global playerButtons
    global reply_markup
    while True:
        reply_markup = reply_markup_maker(playerButtons)
        chat_id, text, update_id = get_last_id_text(get_updates())
        #update_id=update_id + 1
        text = "Choose Player Name"
        send_message(chat_id, text, reply_markup)
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

        while text == 'Choose Player Name':
            sleep(SLEEP_TIME)
            chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
            #chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        #playerButtonAdding(tag)
        global tag
        global auth
        tag=text
        tag=checkForModes(tag,chat_id,update_id)
        if tag == 'Remove Mode':
            continue
        try:
            player = yield from auth.get_player(tag, api.Platforms.UPLAY)
        except:
            chat_id, text, update_id = get_last_id_text(get_updates(update_id))
            send_message(chat_id, "No player found")
            continue
        try:
            rank = yield from player.get_rank("emea")
            chat_id, text, update_id = get_last_id_text(get_updates(update_id))
        except:
            chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
            send_message(chat_id, "Cant fetch the Rank from the Ubisoft Servers")
            continue
        try:
            send_message(chat_id,"Player Skill: " +  str("{0:.2f}".format(round(rank.skill_mean*10, 2))))
        except:
            chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
            send_message(chat_id, "Problems with the Telegram Servers")
            continue
asyncio.get_event_loop().run_until_complete(playerInfo())





# operator = yield from player.get_operator(operatorName)
#  rank=player.load_rank("EU", season=-1)
# print("Kills with "+operatorName+": "+str(operator.kills))