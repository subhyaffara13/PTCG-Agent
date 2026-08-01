
def map_domain(string: str, fn: Callable[[str], str]) -> str:
    parts = string.split("@")
    result = ""
    if len(parts) > 1:
        # In email addresses, only the domain name should be punycoded. Leave
        # the local part (i.e. everything up to `@`) intact.
        result = parts[0] + "@"
        string = parts[1]
    labels = REGEX_SEPARATORS.split(string)
    encoded = ".".join(fn(label) for label in labels)
    return result + encoded

