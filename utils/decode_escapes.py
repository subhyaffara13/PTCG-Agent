
def decode_escapes(regex: Pattern[str], string: str) -> str:
    def decode_match(match: Match[str]) -> str:
        return codecs.decode(match.group(0), "unicode-escape")  # type: ignore

    return regex.sub(decode_match, string)

