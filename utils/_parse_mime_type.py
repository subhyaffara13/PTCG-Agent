
def _parse_mime_type(base64_data: str) -> Optional[str]:
    mime_type_match = re.match(r"data:(.*?);base64", base64_data)
    if mime_type_match:
        return mime_type_match.group(1)
    else:
        return None

