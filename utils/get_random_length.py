import random

def get_random_length(max_sequence_length: int, average_sequence_length: int):
    assert average_sequence_length >= 1 and average_sequence_length <= max_sequence_length

    # For uniform distribution, we find proper lower and upper bounds so that the average is in the middle.
    if 2 * average_sequence_length > max_sequence_length:
        return random.randint(2 * average_sequence_length - max_sequence_length, max_sequence_length)
    else:
        return random.randint(1, 2 * average_sequence_length - 1)

