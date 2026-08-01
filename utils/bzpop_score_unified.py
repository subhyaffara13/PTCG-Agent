
def bzpop_score_unified(response, **options):
    """BZPOPMAX/BZPOPMIN → unified ``[key, member, score]``.

    Works for both RESP2 (bytes score) and RESP3 (float score) wire shapes.
    """
    if not response:
        return None
    return [response[0], response[1], float(response[2])]

