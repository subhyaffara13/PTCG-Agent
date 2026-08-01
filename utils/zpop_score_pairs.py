
def zpop_score_pairs(response, **options):
    """RESP2-wire ZPOPMAX/ZPOPMIN -> legacy ``list[(member, score), ...]``.

    ZPOPMAX/ZPOPMIN always include scores, so this parser intentionally
    does not depend on a ``withscores`` option.
    """
    if not response:
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    it = iter(response)
    return list(zip(it, map(score_cast_func, it)))

