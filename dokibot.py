import os
import time
import pyowm
from slackclient import SlackClient

#DokiBot id from the environment var saved earlier
BOT_ID = os.environ.get("BOT_ID")

#Constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = ""
owm = pyowm.OWM('3c602ac850f9cb0682bad0bd5b1882aa')
#instantiate Slack and Twilo
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

#If message is towards the dokibot this method creates the reply.
def handle_command(command, channel):
    response ="What do you mean? use *" + EXAMPLE_COMMAND + "* command with numbers, delimited by space"
    strQ = "?"
    weatherQ = ","
    if command.endswith(strQ):
        response = command
    if weatherQ in command and command.endswith(strQ):
        weather = retrieveWeather(command)
        response =  weather

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

#Retrieve weather based on city
def retrieveWeather(sentCity):
    city = sentCity.replace("?", "")
    #Searching for weather at place
    forecast = owm.weather_at_place(city)
    w = forecast.get_weather()
    #Getting temperature in Celsius
    weather = "The weather in: " + city + ", is: " + str(w.get_temperature('celsius'))
    return weather

#Checks if the messages sent in the slack channel are directed towards the Dokibot.
def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # One second delay between reading
    #If connection is successfull
    if slack_client.rtm_connect():
        print("YOU MAKE MY HEART GO TOKOROKO DOKI DOKI")
        #Looping through firehose and parsing any messages received
        while True:
            #Parse the output received that our directed to our bot.
            command, channel = parse_slack_output(slack_client.rtm_read())
            #If those messages are directed to the bot, the bot will respond
            if command and channel:
                #Function to handle queries directed to bot.
                handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("We ain't feeling Doki Doki Desu")
