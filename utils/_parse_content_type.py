
def _parse_content_type(content_type: str) -> str:
    m = Message()
    m["content-type"] = content_type
    return m.get_content_type()

