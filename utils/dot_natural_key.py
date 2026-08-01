
def dot_natural_key(s: str):
    """Sort key for state-dict names: split on `"."` and sort digits numerically
    and strings alphabetically. We emit a tuple at each point to sort ints
    first and strings second to avoid int-string comparison failures.
    """
    parts = []
    for part in s.split("."):
        if part.isdigit():
            parts.append((0, int(part)))
        else:
            parts.append((1, part))
    return parts

