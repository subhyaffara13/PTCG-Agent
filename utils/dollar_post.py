
def dollar_post(src: str, end: int) -> bool:
    try:
        nxt = src[end + 1] and charCodeAt(src[end + 1], 0)
    except IndexError:
        return True
    return (
        (not nxt) or (nxt < 0x30) or (nxt > 0x39)
    )  # no decimal digit .. after closing '$'

