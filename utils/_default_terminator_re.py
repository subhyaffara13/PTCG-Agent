import re

def _default_terminator_re() -> re.Pattern[str]:
    return re.compile("[" + re.escape("".join(_DEFAULT_TERMINATORS)) + "]")

