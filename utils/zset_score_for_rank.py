
def zset_score_for_rank(response, **options):
    """
    If ``withscores`` is specified in the options, return the response as
    a [value, score] pair
    """
    if not response or not options.get("withscore"):
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    return [response[0], score_cast_func(response[1])]

