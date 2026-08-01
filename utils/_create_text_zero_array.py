
def _create_text_zero_array(space: Text):
    return "".join(space.characters[0] for _ in range(space.min_length))

