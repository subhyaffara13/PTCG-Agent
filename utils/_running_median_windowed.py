
def _running_median_windowed(iterator, maxlen):
    "Yield median of values in a sliding window."

    window = deque()
    ordered = []

    for x in iterator:
        window.append(x)
        insort(ordered, x)

        if len(ordered) > maxlen:
            i = bisect_left(ordered, window.popleft())
            del ordered[i]

        n = len(ordered)
        m = n // 2
        yield ordered[m] if n & 1 else (ordered[m - 1] + ordered[m]) / 2

