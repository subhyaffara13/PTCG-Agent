import random

def _sample_unweighted(iterator, k, strict):
    # Algorithm L in the 1994 paper by Kim-Hung Li:
    # "Reservoir-Sampling Algorithms of Time Complexity O(n(1+log(N/n)))".

    reservoir = list(islice(iterator, k))
    if strict and len(reservoir) < k:
        raise ValueError('Sample larger than population')
    W = 1.0

    with suppress(StopIteration):
        while True:
            W *= random() ** (1 / k)
            skip = floor(log(random()) / log1p(-W))
            element = next(islice(iterator, skip, None))
            reservoir[randrange(k)] = element

    shuffle(reservoir)
    return reservoir

