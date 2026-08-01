
def no_nans(x):
    if isinstance(x, Series):
        return x.notna().all()
    else:
        return x.notna().all().all()


def no_nans(x):
    return x.notna().all(axis=None)

