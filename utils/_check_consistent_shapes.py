
def _check_consistent_shapes(*arrays):
    all_shapes = {a.shape for a in arrays}
    if len(all_shapes) != 1:
        raise ValueError('The shapes of the passed in arrays do not match')

