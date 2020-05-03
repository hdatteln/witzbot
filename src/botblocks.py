addJokeMessage = {
    'blocks': [{
        'type': 'section',
        'text': {'type': 'mrkdwn', 'text': ':wave: Hi!'}
    }, {
        'type': 'section',
        'text': {'type': 'mrkdwn', 'text': 'To add a new joke, click *Add*'},
        'accessory': {
            'type': 'button',
            'action_id': 'add_joke',
            'style': 'primary',
            'text': {'type': 'plain_text', 'text': 'Add', 'emoji': True},
            'value': 'add_joke_click'
        }
    }]
}

addJokeModal = {
    "type": "modal",
    "title": {
        "type": "plain_text",
        "text": "Witzbot - New Joke",
        "emoji": True
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": True
    },
    "blocks": [
        {
            "type": "input",
            "block_id": "add_joke_block",
            "element": {
                "type": "plain_text_input",
                "action_id": "add_joke_input",
                "multiline": True
            },
            "label": {
                "type": "plain_text",
                "text": "Enter a new joke",
                "emoji": True
            }
        }
    ]
}
