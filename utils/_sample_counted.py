
def _sample_counted(population, k, counts, strict):
    element = None
    remaining = 0

    def feed(i):
        # Advance *i* steps ahead and consume an element
        nonlocal element, remaining

        while i + 1 > remaining:
            i = i - remaining
            element = next(population)
            remaining = next(counts)
        remaining -= i + 1
        return element

    with suppress(StopIteration):
        reservoir = []
        for _ in range(k):
            reservoir.append(feed(0))

    if strict and len(reservoir) < k:
        raise ValueError('Sample larger than population')

    with suppress(StopIteration):
        W = 1.0
        while True:
            W *= random() ** (1 / k)
            skip = floor(log(random()) / log1p(-W))
            element = feed(skip)
            reservoir[randrange(k)] = element

    shuffle(reservoir)
    return reservoir

