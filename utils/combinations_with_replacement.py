import itertools

def combinations_with_replacement(iterable, r, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.combinations_with_replacement`."""
    if total is None:
        try:
            n = len(iterable)
        except (TypeError, AttributeError):
            pass
        else:
            total = 1
            for i in range(n+r-1, n-1, -1):
                total *= i
            for i in range(1, r+1):
                total //= i
    return tqdm_class(itertools.combinations_with_replacement(iterable, r), total=total, **kwargs)

