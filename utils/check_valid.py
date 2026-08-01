
def check_valid(sig, args, kwargs):
    """ Like ``is_valid_args`` for the given signature spec"""
    num_pos_only, func, keyword_exclude, sigspec = sig
    if len(args) < num_pos_only:
        return False
    if keyword_exclude:
        kwargs = dict(kwargs)
        for item in keyword_exclude:
            kwargs.pop(item, None)
    try:
        func(*args, **kwargs)
        return True
    except TypeError:
        return False

