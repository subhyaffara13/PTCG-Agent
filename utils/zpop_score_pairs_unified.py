
def zpop_score_pairs_unified(response, **options):
    """RESP2-wire ZPOPMAX/ZPOPMIN → unified ``list[[member, score], ...]``.

    ZPOPMAX/ZPOPMIN always include scores; no ``withscores`` gate is
    required. Scores are normalised through ``float`` before applying
    ``score_cast_func`` for parity with RESP3.
    """
    if not response:
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    it = iter(response)
    return [[val, score_cast_func(float(score))] for val, score in zip(it, it)]

