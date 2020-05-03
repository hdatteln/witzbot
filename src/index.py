import os
from flask import Flask, request
from slack import WebClient
import ssl as ssl_lib
import certifi
import botblocks
import json

slack_token = os.environ["WB_CLIENT_BOT_TOKEN"]
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Initialize a Web API client
slack_web_client = WebClient(token=slack_token, ssl=ssl_context)


@app.route("/slack/actions", methods=["POST"])
def actions():
    payload = json.loads(request.form["payload"])

    if 'actions' in payload:
        triggered_actions = payload['actions']
        trigger_id = payload['trigger_id']
        for action in triggered_actions:
            if action['action_id'] == 'add_joke':
                add_joke_modal(trigger_id)
    elif 'type' in payload and payload['type'] == 'view_submission':
        payload_val = payload['view']['state']['values']
        if payload_val['add_joke_block'] and payload_val['add_joke_block']['add_joke_input']:
            new_joke = {
                "title": " ",
                "text": payload_val['add_joke_block']['add_joke_input']['value']
            }
            jokes_json = os.path.join(os.path.dirname(__file__), 'data/jokes.json')
            with open(jokes_json) as infile:
                jokes = json.load(infile)
                jokes.append(new_joke)

            with open(jokes_json, 'w') as outfile:
                json.dump(jokes, outfile)

        return {
            'response_action': 'clear'
        }
    else:
        print(payload)

    return {}


def add_joke_modal(trigger_id):
    message_json = botblocks.addJokeModal
    slack_web_client.views_open(trigger_id=trigger_id, view=message_json)
    return {}


def greet(target_channel):
    slack_web_client.chat_postMessage(
        channel=target_channel,
        text='hi'
    )
    return {}


def get_help(target_channel):
    slack_web_client.chat_postMessage(
        channel=target_channel,
        text='To add a new joke: \ntype `@witzbot new joke`'
    )
    return {}


def default_reply(target_channel):
    slack_web_client.chat_postMessage(
        channel=target_channel,
        text='Not sure what you want me to do? To get help: \ntype `@witzbot help`'
    )
    return {}


def add_joke_msg(target_channel):
    message_json = botblocks.addJokeMessage
    message_json['channel'] = target_channel
    slack_web_client.chat_postMessage(**message_json)
    return {}


# Create an event listener for "reaction_added" events and print the emoji name
@app.route("/slack/events", methods=["POST"])
def process_mentions():
    event_data = request.get_json()
    if 'challenge' in event_data:
        return {"challenge": event_data['challenge']}

    evt = event_data['event']
    if evt['type'] == 'app_mention':
        msg_text = evt['text'].lower()
        if 'hello' in msg_text or 'hi ' in msg_text:
            greet(evt['channel'])
        elif 'new joke' in msg_text:
            add_joke_msg(evt['channel'])
        elif 'help' in msg_text:
            get_help(evt['channel'])
        else:
            default_reply(evt['channel'])
    return {}


def main():
    # Start the server on port 3000
    app.run(host='0.0.0.0', port=3001)


if __name__ == "__main__":
    main()
