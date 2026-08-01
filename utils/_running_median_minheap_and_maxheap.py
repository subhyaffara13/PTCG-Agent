
def _running_median_minheap_and_maxheap(iterator):  # pragma: no cover
    "Non-windowed running_median() for Python 3.14+"

    read = iterator.__next__
    lo = []  # max-heap
    hi = []  # min-heap (same size as or one smaller than lo)

    with suppress(StopIteration):
        while True:
            heappush_max(lo, heappushpop(hi, read()))
            yield lo[0]

            heappush(hi, heappushpop_max(lo, read()))
            yield (lo[0] + hi[0]) / 2

