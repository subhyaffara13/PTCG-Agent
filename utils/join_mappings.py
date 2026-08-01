
def join_mappings(**field_to_map):
    """
    Joins multiple mappings together using their common keys.

    >>> user_scores = {'elliot': 50, 'claris': 60}
    >>> user_times = {'elliot': 30, 'claris': 40}
    >>> join_mappings(score=user_scores, time=user_times)
    {'elliot': {'score': 50, 'time': 30}, 'claris': {'score': 60, 'time': 40}}
    """
    ret = defaultdict(dict)

    for field_name, mapping in field_to_map.items():
        for key, value in mapping.items():
            ret[key][field_name] = value

    return dict(ret)

