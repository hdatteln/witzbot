import json
from random import randint


def get_random_joke_from_file(file_path):
    """
    Get a random joke from a json file.
    The json needs to have the format [{"title": "joke title", "text": "joke text"},...].
    :param file_path: The json file path.
    :return: One joke from json file, picked at random
    """

    with open(file_path) as f:
        jokes = json.load(f)
    num_jokes = len(jokes)
    random_index = randint(0, num_jokes -1)
    return jokes[random_index]
