import os
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
import jokes
import schedule
import time

client_id = os.environ["WB_CLIENT_ID"]
client_signing_secret = os.environ["WB_CLIENT_SIGNING_SECRET"]
slack_token = os.environ["WB_CLIENT_BOT_TOKEN"]
joke_channel = os.environ["WB_DEFAULT_CHANNEL"]
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(client_signing_secret, "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=slack_token, ssl=ssl_context)


def tell_random_joke():
    jokes_json = os.path.join(os.path.dirname(__file__), 'data/jokes.json')
    joke = jokes.get_random_joke_from_file(jokes_json)
    msg = "*{0}*\n{1}".format(joke['title'], joke['text'])
    response = slack_web_client.chat_postMessage(
        channel=joke_channel,
        text=msg
    )
    return response


def job_tell_joke():
    curr_time = round(time.time())
    if curr_time % 4 == 0:
        tell_random_joke()


def main():
    schedule.every(20).minutes.do(tell_random_joke)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
