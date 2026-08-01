
def extract_fnam_from_message(message: str) -> str | None:
    m = re.match(r"([^:]+):[0-9]+: (error|note): ", message)
    if m:
        return m.group(1)
    return None

