import os
from slackclient import SlackClient

BOT_NAME = 'dokibot'

#Get the token for our slack channel
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
    #Make an api call to retrieve a list of users.
    api_call =  slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users
        users = api_call.get('members')
        #Looping through ever user in the list of users on the slack channel to
        #Find the username that corresponds to our BOT and then printing that username
        #alongside with the id.
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "'is " + user.get('id'))
            else:
                print("Can't find your bot with id: " + user.get('id'))
