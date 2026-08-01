
def _multiset_histogram(n):
    """Return tuple used in permutation and combination counting. Input
    is a dictionary giving items with counts as values or a sequence of
    items (which need not be sorted).

    The data is stored in a class deriving from tuple so it is easily
    recognized and so it can be converted easily to a list.
    """
    if isinstance(n, dict):  # item: count
        if not all(isinstance(v, int) and v >= 0 for v in n.values()):
            raise ValueError
        tot = sum(n.values())
        items = sum(1 for k in n if n[k] > 0)
        return _MultisetHistogram([n[k] for k in n if n[k] > 0] + [items, tot])
    else:
        n = list(n)
        s = set(n)
        lens = len(s)
        lenn = len(n)
        if lens == lenn:
            n = [1]*lenn + [lenn, lenn]
            return _MultisetHistogram(n)
        m = dict(zip(s, range(lens)))
        d = dict(zip(range(lens), (0,)*lens))
        for i in n:
            d[m[i]] += 1
        return _multiset_histogram(d)

