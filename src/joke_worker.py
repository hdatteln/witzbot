import os
from slack import WebClient
import ssl as ssl_lib
import certifi
import jokes
import schedule
import time

slack_token = os.environ["WB_CLIENT_BOT_TOKEN"]
joke_channel = os.environ["WB_DEFAULT_CHANNEL"]
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

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
    if curr_time % 5 == 0:
        tell_random_joke()


def main():
    schedule.every(35).minutes.do(job_tell_joke)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
