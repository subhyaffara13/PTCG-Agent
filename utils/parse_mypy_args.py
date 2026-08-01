
def parse_mypy_args(line: str) -> list[str]:
    m = re.match("# flags: (.*)$", line)
    if not m:
        return []  # No args; mypy will spit out an error.
    return m.group(1).split()

