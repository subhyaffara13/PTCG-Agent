import re
from typing import Any

def pattern_validator(v: Any) -> Pattern[str]:
    if isinstance(v, Pattern):
        return v

    str_value = str_validator(v)

    try:
        return re.compile(str_value)
    except re.error:
        raise errors.PatternError()

