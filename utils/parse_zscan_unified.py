
def parse_zscan_unified(response, **options):
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    cursor, r = response
    it = iter(r)
    return int(cursor), [
        [value, score_cast_func(float(score))] for value, score in zip(it, it)
    ]

