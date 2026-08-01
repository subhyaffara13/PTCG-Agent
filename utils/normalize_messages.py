
def normalize_messages(messages: list[str]) -> list[str]:
    return [re.sub("^tmp" + re.escape(os.sep), "", message) for message in messages]

