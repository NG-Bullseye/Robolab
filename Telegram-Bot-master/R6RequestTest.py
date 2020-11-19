from pprint import pprint
import requests
import json
from time import sleep
from R6Info import *
# from tele_news import *
# from tele_saavn import *
from tele_temp import temp

# from tele_news import info

SLEEP_TIME = 0.2
token = '585021350:AAEciXskrmka0wp1xejUsi792YFLiTcg_xY'
url = 'https://api.telegram.org/bot{}/'.format(token)
init = 't'
tag = ''
rosterButtons = ['Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5']
# menuButtons = ['Roster','Player Info','Esl News','you mom gay']
menuButtons = ['watch Roster', 'add Player']


def getme():
    res = requests.get(url + "getme")
    d = res.json()
    username = d['result']['username']
    return username


def get_updates(offset=None):
    while True:
        try:
            URL = url + 'getUpdates'
            if offset:
                URL += '?offset={}'.format(offset)

            res = requests.get(URL)
            while (res.status_code != 200 or len(res.json()['result']) == 0):
                sleep(1)
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


def ask_contact(chat_id):
    print('Ask Contact')
    text = 'Send Contact'
    keyboard = [[{"text": "Contact", "request_contact": True}]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    send_message(chat_id, text, json.dumps(reply_markup))


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


def roster(chat_id, update_id):
    message = 'Choose Slot!'
    global init
    global rosterButtons
    # get current sloting
    #commands = [slot1, slot2, slot3, slot4, slot5]
    reply_markup = reply_markup_maker(rosterButtons)
    send_message(chat_id, message, reply_markup)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'Choose Slot!':
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    slot=text
    if text.lower() == 'slot 1'or'slot 2'or'slot 3'or'slot 4'or'slot 5':
        if 	 slot=='Slot 1':
            rosterButtons[0] = tag
        elif text=='Slot 2':
            rosterButtons[1] = tag
        elif text=='Slot 3':
            rosterButtons[2] = tag
        elif text=='Slot 4':
            rosterButtons[3] = tag
        elif text=='Slot 5':
            rosterButtons[4] = tag

    if tag.lower() in slot.lower():
        reply_markup = reply_markup_maker(['Delete','Change'])
        send_message(chat_id, "Make a choise", reply_markup)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
        while text.lower() == 'Make a choise':
            chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
            sleep(SLEEP_TIME)
        if text.lower() == 'delete' or 'change':
            i = 0
            while i < len(rosterButtons):
                if tag in rosterButtons[i] :
                    if text == 'Delete':
                        rosterButtons[i] = 'Slot ' + str(i + 1)
                        message = 'Good luck and dont forget to Preaim and Prefire!!'
                        send_message(chat_id, message, None)
                        return
                    elif text == 'Change':
                        slot='Slot '+str(i+1)
                        break
                i=i+1
    sleep(SLEEP_TIME)
    message = 'When can you start?'
    send_message(chat_id, message, None)
    chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'when can you start?':
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
    i=0
    while i < len(rosterButtons):
        if tag in rosterButtons[i]:
            rosterButtons[i] = 'Slot ' + str(i + 1)
            break
        i=i+1
    time = text
    if 	 slot=='Slot 1':
        rosterButtons[0] = tag + ': ' + time
    elif slot=='Slot 2':
        rosterButtons[1] = tag + ': ' + time
    elif slot=='Slot 3':
        rosterButtons[2]= tag + ': ' + time
    elif slot=='Slot 4':
        rosterButtons[3] = tag + ': ' + time
    elif slot=='Slot 5':
        rosterButtons[4] = tag + ': ' + time
    #commands = [slot1, slot2, slot3, slot4, slot5]
    message='Good luck and dont forget to Preaim and Prefire!!'
    sleep(SLEEP_TIME)
    send_message(chat_id, message, None)

def start(chat_id):
    text = "Personal Assistance to your Command"
    sleep(SLEEP_TIME)
    send_message(chat_id, text)
    chat_id, text, update_id = get_last_id_text(get_updates())
    text = 'Enter Name'
    sleep(SLEEP_TIME)
    send_message(chat_id, text, None)
    while text == 'Enter Name':
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))
    global tag
    tag = text
    return chat_id, text, update_id

def main():
    text= ''
    #print('Calling for the Assistance')
    chat_id, text, update_id = get_last_id_text(get_updates())
    start(chat_id)
    loopcount=0
    while True:
        sleep(SLEEP_TIME)
        chat_id, text, update_id = get_last_id_text(get_updates())
        #roster(chat_id, update_id)
        send_message(chat_id, playerInfo(tag),None)
        chat_id, text, update_id = get_last_id_text(get_updates(update_id + 1))

        loopcount=loopcount+1
        print("Main loop counter: "+str(loopcount))

asyncio.get_event_loop().run_until_complete(main())