
def _special_token_regex(tokens: frozenset[str]) -> re.Pattern[str]:
    try:
        import regex as re
    except ImportError:
        import re
    inner = "|".join(re.escape(token) for token in tokens)
    return re.compile(f"({inner})")

