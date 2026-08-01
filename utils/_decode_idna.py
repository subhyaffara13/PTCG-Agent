
def _decode_idna(domain: str) -> str:
    try:
        data = domain.encode("ascii")
    except UnicodeEncodeError:
        # If the domain is not ASCII, it's decoded already.
        return domain

    try:
        # Try decoding in one shot.
        return data.decode("idna")
    except UnicodeDecodeError:
        pass

    # Decode each part separately, leaving invalid parts as punycode.
    parts = []

    for part in data.split(b"."):
        try:
            parts.append(part.decode("idna"))
        except UnicodeDecodeError:
            parts.append(part.decode("ascii"))

    return ".".join(parts)

