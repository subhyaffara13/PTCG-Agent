
def parse_geopos_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire GEOPOS → legacy RESP2 ``list[tuple(float, float) | None]``.

    Matches today's RESP2-wire callback shape (tuple coordinates).
    """
    return [(float(ll[0]), float(ll[1])) if ll is not None else None for ll in response]

