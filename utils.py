import random
import string


def generate_random_hash(length=5):
    characters = string.ascii_letters + string.digits
    hash_str = ""

    for _ in range(length):
        random_index = random.randint(0, len(characters) - 1)
        hash_str += characters[random_index]

    return hash_str
