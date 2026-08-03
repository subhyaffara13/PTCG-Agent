import itertools
import math


def combinations(iterable, r, total=None, tqdm_class=tqdm_auto, **kwargs):
    """Equivalent of `itertools.combinations`."""
    if total is None:
        try:
            n = len(iterable)
        except (TypeError, AttributeError):
            pass
        else:
            if r > n:
                total = 0
            else:
                total = math.comb(n, r)
    return tqdm_class(itertools.combinations(iterable, r), total=total, **kwargs)


def combinations(seqs):
    """

    Recipe 496807 from ActiveState Python CookBook

    Non recursive technique for getting all possible combinations of a sequence
    of sequences.

    """

    r = [[]]
    for x in seqs:
        r = [i + [y] for y in x for i in r]
    return r

