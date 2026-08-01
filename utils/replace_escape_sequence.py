
def replace_escape_sequence(match: Match[str]) -> str:
    return ESCAPE_SEQUENCES[match.group(0)]

