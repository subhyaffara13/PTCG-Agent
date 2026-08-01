
def _pd_nsamples(kwargs):
    return 2 if kwargs.get('f_exp', None) is not None else 1

