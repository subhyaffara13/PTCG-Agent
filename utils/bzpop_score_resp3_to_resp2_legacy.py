
def bzpop_score_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire BZPOPMAX/BZPOPMIN → legacy RESP2 ``(key, member, score)``.

    Matches the v8.0.0b1 RESP2-wire callback shape (tuple, ``float`` score).
    """
    if not response:
        return None
    return (response[0], response[1], float(response[2]))

