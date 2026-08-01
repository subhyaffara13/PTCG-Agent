
def extract_possible_fnam_from_message(message: str) -> str:
    # This may return non-path things if there is some random colon on the line
    return message.split(":", 1)[0]

