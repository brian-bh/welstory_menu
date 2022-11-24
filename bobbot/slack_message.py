from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
import os
import welstory
import menu_image

load_dotenv(verbose=True)
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
this = Path(__file__).parent.absolute()

def postMessage(message):
    client = WebClient(token=SLACK_APP_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            type="mrkdwn",
            text=message)
        return response['ts']
    except SlackApiError as e:
        assert e.response["error"]

def postMessageWithFiles(message, fileList, ts):
    client = WebClient(token=SLACK_APP_TOKEN)
    for file in fileList:
        upload = client.files_upload(file=file, filename=file)
        message += "<" + upload['file']['permalink'] + "| >"
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            type="mrkdwn",
            text=message,
            thread_ts=ts)
    except SlackApiError as e:
        assert e.response["error"]

def send_message_to_slack():
    msg = ""
    msg2 = ""
    msg += f"오늘의 구내식당 점심 메뉴\n"
    menu_list = welstory.welstory_parse()
    filelister = []
    if menu_list == 'no menu':
        print(menu_list)
    else:
        for a in menu_list:
            menu_image.menu_image_download(a)
            if a['when'] != '점심':
                continue
            msg += f"\n\n• *{a['name']}* ({a['where']})"
            msg2 += f"\n\n• *{a['name']}* ({a['where']}) : (구성: {a['submenu']} / {a['kcal']} 칼로리)"
            if a['photo'] is not None:
                filelister.append(f"{a['where']}.png")
    postMessageWithFiles(msg2, filelister, postMessage(msg))
    for fi in this.glob("*.png"):
        os.remove(Path(fi).name)
