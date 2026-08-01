
def _read_payload_from_msg(msg: Message) -> str | None:
    value = str(msg.get_payload()).strip()
    if value == 'UNKNOWN' or not value:
        return None
    return value

