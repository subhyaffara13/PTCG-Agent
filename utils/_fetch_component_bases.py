
def _fetchComponentBases(glif: bytes) -> list[str]:
    """
    Get a list of component base glyphs listed in glif.
    """
    parser = _FetchComponentBasesParser()
    try:
        parser.parse(glif)
    except _DoneParsing:
        pass
    return list(parser.bases)

