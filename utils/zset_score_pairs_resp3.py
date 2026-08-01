
def zset_score_pairs_resp3(response, **options):
    """
    If ``withscores`` is specified in the options, return the response as
    a list of [value, score] pairs
    """
    if not response or not options.get("withscores"):
        return response
    score_cast_func = options.get("score_cast_func", float)
    return [[name, score_cast_func(val)] for name, val in response]

