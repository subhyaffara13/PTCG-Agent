
def any_score_callable(t: CallableType, is_method: bool, ignore_return: bool) -> float:
    # Ignore the first argument of methods
    scores = [any_score_type(x, arg_pos=True) for x in t.arg_types[int(is_method) :]]
    # Return type counts twice (since it spreads type information), unless it is
    # None in which case it does not count at all. (Though it *does* still count
    # if there are no arguments.)
    if not isinstance(get_proper_type(t.ret_type), NoneType) or not scores:
        ret = 1.0 if ignore_return else any_score_type(t.ret_type, arg_pos=False)
        scores += [ret, ret]

    return sum(scores) / len(scores)

