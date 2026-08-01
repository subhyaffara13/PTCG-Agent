
def zmpop_unified(response, **options):
    """ZMPOP/BZMPOP → unified ``[name, [[member, float_score], ...]]``.

    Used for the ``legacy_responses=False`` overlay on RESP2 wire to mirror
    RESP3's native float-score shape.
    """
    if not response:
        return response
    return [
        response[0],
        [[member, float(score)] for member, score in response[1]],
    ]

