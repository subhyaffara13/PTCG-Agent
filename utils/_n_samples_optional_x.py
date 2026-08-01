
def _n_samples_optional_x(kwargs):
    return 2 if kwargs.get('x', None) is not None else 1

