
def cycle_edges(c):
    return pairwise(chain(c, islice(c, 1)))

