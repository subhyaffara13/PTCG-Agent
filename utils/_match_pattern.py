
def _match_pattern(match: Pattern[str]) -> str | Pattern[str]:
    """Helper function to remove redundant `re.compile` calls when printing regex"""
    return match.pattern if match.flags == _REGEX_NO_FLAGS else match

