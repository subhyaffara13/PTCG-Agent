
def sample_iter_lambdify(expr, condition=None, size=(),
                         numsamples=S.Infinity, seed=None, **kwargs):

    return sample_iter(expr, condition=condition, size=size,
                       numsamples=numsamples, seed=seed, **kwargs)

