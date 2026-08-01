
def get_public_names(values: Iterable[str]) -> list[str]:
    """Only return names from iterator values without a leading underscore."""
    return [x for x in values if x[0] != "_"]

