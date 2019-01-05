import logging
from localsettings import *

import requests
import pandas as pd

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Telegram:

    def __init__(self, token=telegram_token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(telegram_token)

    def get_updates(self, offset=None, timeout=30):
            method = 'getUpdates'
            params = {'timeout': timeout, 'offset': offset}
            resp = requests.get(self.api_url + method, params)
            result_json = resp.json()['result']
            return result_json

    @classmethod
    def messagepermitted(cls, msg):
        match_id, alert_type, msg_text = msg

        messages = pd.read_csv(path + 'messages.csv')
        sent_messages = messages[
            (messages['match_id'].astype(str) == match_id) & (messages['alert_type'].astype(str) == alert_type)]

        return sent_messages.empty

    def send_message(self, chat_id, msg):

        print('trying to send a Telegram about {}'.format(msg[2]))

        resp= ''
        messages = pd.read_csv(path + 'messages.csv')

        if Telegram.messagepermitted(msg):
            match_id, alert_type, msg_text = msg

            params = {'chat_id': chat_id, 'text': msg_text}
            method = 'sendMessage'
            resp = requests.post(self.api_url + method, params)

            row = list(map(str.strip, [match_id, alert_type, '']))
            messages = messages.append(pd.DataFrame([row], columns=['match_id', 'alert_type', 'user_id']), ignore_index=True)

        messages.to_csv(path + 'messages.csv', index=False)

        return resp

    def get_last_update(self):

        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


