
def parse_geopos_unified(response, **options):
    """GEOPOS → unified ``list[list[float, float] | None]``.

    Used for the ``legacy_responses=False`` overlay on RESP2 wire to mirror
    RESP3's native ``list[list]`` shape.
    """
    return [[float(ll[0]), float(ll[1])] if ll is not None else None for ll in response]

