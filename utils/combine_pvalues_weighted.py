
def combine_pvalues_weighted(*args, **kwargs):
    return stats.combine_pvalues(args[0], *args[2:], weights=args[1],
                                 method='stouffer', **kwargs)

