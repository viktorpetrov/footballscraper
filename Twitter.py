import twitter

api = twitter.Api(consumer_key='SM4UDZ5OtiIN5lU485NN4P6Et',
                  consumer_secret='91haQ7aywkRFwq1pfS4hgXKiKWcQwYm6OTu0dQpM3FZv4z4F95',
                  access_token_key='442751368-YfuMBADigYkuIkXEtVLrpYtJDRF7kpgyb52dau0m',
                  access_token_secret='blha8TWEfO2rjpHFwqQk46qD9nICu9O8tXkUtVDSbQFlE'
                  )

#jepperm 1208132010
#ik 442751368

class TwitterMsg:

    def __init__(self):
        print('initiating TwitterMsg')

    def sendDM(self,userids, msg):

        for user in userids:
            send_msg = api.PostDirectMessage(msg, user_id=user, return_json=True)
            print(send_msg)