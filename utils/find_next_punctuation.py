
def find_next_punctuation(text: str, start_idx=0):
    """
    Find the index of the next punctuation mark.

    Args:
        text (`str`):
            String to examine
        start_idx (`int`, *optional*)
            Index where to start
    """

    for i in range(start_idx, len(text)):
        if text[i] in [".", "?", "!", "\n"]:
            return i

    return None

