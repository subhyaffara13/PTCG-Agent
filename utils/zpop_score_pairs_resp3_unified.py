
def zpop_score_pairs_resp3_unified(response, **options):
    """RESP3-wire ZPOPMAX/ZPOPMIN → unified ``list[[member, score], ...]``.

    Without ``count`` RESP3 returns a flat ``[member, score]``; with
    ``count`` it returns a nested ``[[member, score], ...]``. Both shapes
    are normalised to a nested list with ``score_cast_func`` applied.
    """
    if not response:
        return response
    score_cast_func = options.get("score_cast_func", float)
    if isinstance(response[0], list):
        return [[name, score_cast_func(val)] for name, val in response]
    return [[response[0], score_cast_func(response[1])]]

