
def _replace_escape_sequence(match):
    return ESCAPE_SEQUENCES[match.group(0)]

