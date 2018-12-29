import twitter
import pandas as pd

api = twitter.Api(consumer_key='SM4UDZ5OtiIN5lU485NN4P6Et',
                  consumer_secret='91haQ7aywkRFwq1pfS4hgXKiKWcQwYm6OTu0dQpM3FZv4z4F95',
                  access_token_key='442751368-YfuMBADigYkuIkXEtVLrpYtJDRF7kpgyb52dau0m',
                  access_token_secret='blha8TWEfO2rjpHFwqQk46qD9nICu9O8tXkUtVDSbQFlE'
                  )

#jepperm 1208132010
#ik 442751368

path = '/Users/vpetrov/PycharmProjects/FootballAPI/'

class TwitterMsg:
    
    def __init__(self):
        pass

    @classmethod
    def messagepermitted(self,msg,user_id):
        match_id = msg[0]
        alert_type = msg[1]

        messages = pd.read_csv(path + 'messages.csv')
        sent_messages = messages[(messages['match_id'].astype(str) == match_id) & (messages['alert_type'].astype(str) == alert_type) & (messages['user_id'].astype(str) == user_id)]
        print('found {} sent message about this game'.format(len(sent_messages)))
        
        return sent_messages.empty

    def senddm(self, userids, msg):
        
        messages = pd.read_csv(path + 'messages.csv')

        for user_id in userids:
            if TwitterMsg.messagepermitted(msg,user_id):
                match_id = msg[0]
                alert_type = msg[1]
                msg_text = msg[2]
                
                send_msg = api.PostDirectMessage(msg_text, user_id=user_id, return_json=True)
                print(send_msg)
                row = list(map(str.strip, [match_id,alert_type,user_id]))
                messages = messages.append(pd.DataFrame([row], columns=['match_id','alert_type','user_id']), ignore_index=True)

        messages.to_csv(path + 'messages.csv', index=False)