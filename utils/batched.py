import itertools

def batched(iterable, n, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.batched`."""
    if total is None:
        try:
            total = len(iterable)
        except (TypeError, AttributeError):
            pass
    return tqdm_class(itertools.batched(iterable, n), unit_scale=n,
                      total=(total+n-1) // n if total is not None else None,
                      **kwargs)

