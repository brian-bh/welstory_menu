from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime

from src import config

SLACK_APP_TOKEN = config.SLACK_APP_TOKEN
SLACK_CHANNEL_ID = config.SLACK_CHANNEL_ID


def post_message(message):
    client = WebClient(token=SLACK_APP_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            type="mrkdwn",
            text=message)
        return response
    except SlackApiError as e:
        assert e.response["error"]


def post_message_with_files(message, file_list, ts):
    client = WebClient(token=SLACK_APP_TOKEN)
    for file in file_list:
        upload = client.files_upload(
            file=str(file['filepath']),
            filename=file['filename'],
            initial_comment=f'{datetime.datetime.now()}'
        )
        message += "<" + upload['file']['permalink'] + "| >"
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            type="mrkdwn",
            text=message,
            thread_ts=ts)
        return response
    except SlackApiError as e:
        assert e.response["error"]