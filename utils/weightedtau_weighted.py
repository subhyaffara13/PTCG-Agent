
def weightedtau_weighted(x, y, rank, **kwargs):
    axis = kwargs.get('axis', 0)
    nan_policy = kwargs.get('nan_policy', 'propagate')
    rank = stats.rankdata(rank, axis=axis, nan_policy=nan_policy)
    return stats.weightedtau(x, y, rank, **kwargs)

