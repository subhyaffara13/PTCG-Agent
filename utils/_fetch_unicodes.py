
def _fetchUnicodes(glif: bytes) -> list[int]:
    """
    Get a list of unicodes listed in glif.
    """
    parser = _FetchUnicodesParser()
    parser.parse(glif)
    return parser.unicodes

