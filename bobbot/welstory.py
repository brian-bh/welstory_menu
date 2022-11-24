import json
import os
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import datetime

load_dotenv(verbose=True)
now = datetime.datetime.today()
now_s = now.strftime("%Y%m%d")

def welstory_parse():
    WELSTORY_ID = os.getenv('WELSTORY_ID')
    WELSTORY_PW = os.getenv('WELSTORY_PW')
    WELSTORY_RESTAURANT = os.getenv('WELSTORY_RESTAURANT_CODE')
    sql = 'fetch("https://welplus.welstory.com/login", {  "headers": {    "accept": "application/json, text/plain, ' \
          '*/*",    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",    "content-type": ' \
          '"application/x-www-form-urlencoded;charset=UTF-8",' \
          '"sec-fetch-dest": "empty",    "sec-fetch-mode": "cors",    ' \
          '"sec-fetch-site": "same-origin"  },  "referrer": "https://welplus.welstory.com/",  "referrerPolicy": ' \
          f'"strict-origin-when-cross-origin",  "body": "username={WELSTORY_ID}&password={WELSTORY_PW}&remember-me=false",  ' \
          '"method": "POST",  "mode": "cors",  "credentials": "include"}); '
    with sync_playwright() as playwright:
        nexus_10 = playwright.devices['Nexus 10']
        browser = playwright.chromium.launch()
        context = browser.new_context(**nexus_10)
        page = context.new_page()
        page.goto('https://welplus.welstory.com/')
        page.evaluate(sql)
        site = f'https://welplus.welstory.com/api/meal?menuDt={now_s}&menuMealType=2&restaurantCode={WELSTORY_RESTAURANT}' \
               f'&sortingFlag=basic '
        page.goto(site)
        page_source = page.content()
        soup = BeautifulSoup(page_source, 'html.parser').get_text()
        try:
            j = json.loads(soup)
        except:
            return 'no menu'
        menu = []
        for menus in j["data"]["mealList"]:
            if menus['photoCd'] is not None and menus['photoUrl'] is not None:
                name = menus['menuName']
                where = menus['courseTxt']
                photo = menus['photoUrl'] + menus['photoCd']
                submenu = menus['subMenuTxt']
                when = menus['menuMealTypeTxt']
                kcal = menus['sumKcal']
                listup = {'name': name, 'photo': photo, 'where': where, 'when': when, 'submenu': submenu, 'kcal': kcal}
                menu.append(listup)
            else:
                name = menus['menuName']
                where = menus['courseTxt']
                submenu = menus['subMenuTxt']
                when = menus['menuMealTypeTxt']
                kcal = menus['sumKcal']
                listup = {'name': name, 'photo': None, 'where': where, 'when': when, 'submenu': submenu, 'kcal': kcal}
                menu.append(listup)
        return menu