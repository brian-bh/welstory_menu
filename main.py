from src.bobbot import welstory
from src.bobbot import menu_image
from src.messenger import slack_util as slack
import os
import logging
from pathlib import Path

image_path = Path('.', 'menu_images')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 슬랙으로 메시지 보내는 기능
def send_message_to_slack():
    msg = ""
    msg2 = ""
    msg += f"오늘의 구내 식당 점심 메뉴\n"
    menu_list = welstory.welstory_parse()
    filelister = []
    if menu_list == 'no menu':
        logger.warning(f'메뉴를 불러오지 못 했습니다.')
    else:
        for a in menu_list:
            menu_image.menu_image_download(a)
            if a['when'] != '점심':
                continue
            msg += f"\n\n• *{a['name']}* ({a['where']})"
            msg2 += f"\n\n• *{a['name']}* ({a['where']}) : (구성: {a['submenu']} / {a['kcal']} 칼로리)"
            if a['photo'] is not None:
                filelister.append({
                    'filename': f"{a['where']}.png",
                    'filepath': Path.joinpath(image_path, f"{a['where']}.png")
                })
    inf = slack.post_message_with_files(msg2, filelister, slack.post_message(msg)['ts'])
    logger.info(f'{inf}')


def flush_menu_images():
    for fi in image_path.glob("*.png"):
        os.remove(Path.joinpath(image_path, Path(fi).name))
    logger.info("image files flushed.")


if __name__ == "__main__":
    send_message_to_slack()
    flush_menu_images()
