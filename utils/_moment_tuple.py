
def _moment_tuple(x, n_out):
    return tuple(x[i, ...] for i in range(x.shape[0])) if n_out > 1 else (x,)

