
def get_known_facts_keys():
    """
    Return every unary predicates registered to ``Q``.

    This function is used to generate the keys for
    ``generate_known_facts_dict``.

    """
    # exclude polyadic predicates
    exclude = {Q.eq, Q.ne, Q.gt, Q.lt, Q.ge, Q.le}

    result = []
    for attr in Q.__class__.__dict__:
        if attr.startswith('__'):
            continue
        pred = getattr(Q, attr)
        if pred in exclude:
            continue
        result.append(pred)
    return result

