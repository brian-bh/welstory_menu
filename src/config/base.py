from dotenv import load_dotenv
import os

load_dotenv()


def _get_environment_variable(var_name, default=None):
    try:
        value = os.getenv(var_name)

    except KeyError:
        raise f'Environment Key {var_name} does not exist in .env file'
        return default

    return value


WELSTORY_ID = _get_environment_variable('WELSTORY_ID')
WELSTORY_PW = _get_environment_variable('WELSTORY_PW')
SLACK_APP_TOKEN = _get_environment_variable('SLACK_APP_TOKEN')
SLACK_CHANNEL_ID = _get_environment_variable('SLACK_CHANNEL_ID')
WELSTORY_RESTAURANT_CODE = _get_environment_variable('WELSTORY_RESTAURANT_CODE')
