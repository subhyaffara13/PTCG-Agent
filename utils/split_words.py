
def split_words(msg: str) -> list[str]:
    """Split line of text into words (but not within quoted groups)."""
    next_word = ""
    res: list[str] = []
    allow_break = True
    for c in msg:
        if c == " " and allow_break:
            res.append(next_word)
            next_word = ""
            continue
        if c == '"':
            allow_break = not allow_break
        next_word += c
    res.append(next_word)
    return res

