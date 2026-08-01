
def welford(mean, m2, weight, dim):
    return tl.reduce((mean, m2, weight), dim, welford_combine)

