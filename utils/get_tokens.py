
def get_tokens(tokens_string):
    """
    Return an iterable of strings splitting on spaces and parens.
    """
    return [match for match in _tokenizer.split(tokens_string.lower()) if match]


def get_tokens(s):
    if not s:
        return []
    return normalize_answer(s).split()

