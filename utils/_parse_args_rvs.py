
def _parse_args_rvs(self, p, loc=0, size=None):
    return tuple(np.moveaxis(p, -1, 0)), loc, 1.0, size

