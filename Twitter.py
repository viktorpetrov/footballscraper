import twitter
import pandas as pd
from localsettings import *

#jepperm 1208132010
#ik 442751368

class TwitterMsg:

    api = twitter.Api(consumer_key=twitter_consumer_key,
                      consumer_secret=twitter_consumer_secret,
                      access_token_key=twitter_access_token_key,
                      access_token_secret=twitter_access_token_secret
                      )
    
    def __init__(self):
        pass

    @classmethod
    def messagepermitted(cls,msg,user_id):
        match_id = msg[0]
        alert_type = msg[1]

        messages = pd.read_csv(path + 'messages.csv')
        sent_messages = messages[(messages['match_id'].astype(str) == match_id) & (messages['alert_type'].astype(str) == alert_type) & (messages['user_id'].astype(str) == user_id)]
        
        return sent_messages.empty

    def senddm(self, userids, msg):
        
        messages = pd.read_csv(path + 'messages.csv')

        for user_id in userids:
            if TwitterMsg.messagepermitted(msg,user_id):
                match_id, alert_type, msg_text = msg

                send_msg = TwitterMsg.api.PostDirectMessage(msg_text, user_id=user_id, return_json=True)
                print('Sent Twitter DM: {}'.format(send_msg['event']['id']))
                if send_msg['event']['id']:
                    row = list(map(str.strip, [match_id,alert_type,user_id]))
                    messages = messages.append(pd.DataFrame([row], columns=['match_id','alert_type','user_id']), ignore_index=True)

        messages.to_csv(path + 'messages.csv', index=False)