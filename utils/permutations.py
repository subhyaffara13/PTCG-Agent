
def permutations(iterable, r=None, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.permutations`."""
    if total is None:
        try:
            n = len(iterable)
        except (TypeError, AttributeError):
            pass
        else:
            r = n if r is None else r
            if r > n:
                total = 0
            else:
                total = math.perm(n, r)
    return tqdm_class(itertools.permutations(iterable, r), total=total, **kwargs)

