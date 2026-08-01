
def query_to_pairs(query_string: str) -> list[tuple[str, str]]:
    """Parse a query given as a string argument.

    Works like urllib.parse.parse_qsl with keep empty values.
    """
    pairs: list[tuple[str, str]] = []
    if not query_string:
        return pairs
    for k_v in query_string.split("&"):
        k, _, v = k_v.partition("=")
        pairs.append((UNQUOTER_PLUS(k), UNQUOTER_PLUS(v)))
    return pairs

