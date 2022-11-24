WELSTORY MENU
=======
--------
삼성웰스토리 앱의 모바일 페이지를 playwright을 이용해 구현하여 딕셔너리로 파싱하는 스크립트입니다. (welstory.py)\
menu_image.py에는 Pillow를 이용, 메뉴 사진들을 다운받고 어떤 메뉴인지, 칼로리는 어떻게 되는지 적어서 만들어주는 스크립트가 있습니다.\
slack_message.py는 Slack 메신저에 올려주는 기능입니다.\
(추후 변경 예정) .env를 .env.example 참고하여 적어넣고, slack_message.py의 send_message_to_slack 함수를 실행하면 됩니다.