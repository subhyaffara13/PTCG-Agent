import re
from typing import Callable

def _parse_stack_trace(
    stack_trace: str, filter_fn: Callable[[str, str, str], bool] | None = None
):
    if stack_trace is None:
        return None
    pattern = re.compile(r"^File \"(.+)\", line (\d+), in (.+)$")
    lines = stack_trace.strip().split("\n")
    # stacktrace should have innermost frame last, so we
    # iterate backwards to find the first line that starts
    # with 'File '
    for idx in range(len(lines) - 2, -1, -1):
        line = lines[idx].strip()
        matches = pattern.match(line)
        if matches:
            file = matches.group(1)
            lineno = matches.group(2)
            name = matches.group(3)
            # next line should be the code
            code = lines[idx + 1].strip()
            if filter_fn and not filter_fn(file, name, code):
                continue
            return _ParsedStackTrace(file, lineno, name, code)
    return None

