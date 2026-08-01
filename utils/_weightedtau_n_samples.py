
def _weightedtau_n_samples(kwargs):
    rank = kwargs.get('rank', False)
    return 2 if (isinstance(rank, bool) or rank is None) else 3

