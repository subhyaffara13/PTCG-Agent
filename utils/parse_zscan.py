
def parse_zscan(response, **options):
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    cursor, r = response
    it = iter(r)
    return int(cursor), list(zip(it, map(score_cast_func, it)))

