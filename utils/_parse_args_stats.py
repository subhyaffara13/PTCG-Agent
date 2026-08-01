
def _parse_args_stats(self, p, loc=0, moments='mv'):
    return tuple(np.moveaxis(p, -1, 0)), loc, 1.0, moments

