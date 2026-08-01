
def _running_median_minheap_only(iterator):  # pragma: no cover
    "Backport of non-windowed running_median() for Python 3.13 and prior."

    read = iterator.__next__
    lo = []  # max-heap (actually a minheap with negated values)
    hi = []  # min-heap (same size as or one smaller than lo)

    with suppress(StopIteration):
        while True:
            heappush(lo, -heappushpop(hi, read()))
            yield -lo[0]

            heappush(hi, -heappushpop(lo, -read()))
            yield (hi[0] - lo[0]) / 2

