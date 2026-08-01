
def all_na(x):
    if isinstance(x, Series):
        return x.isnull().all()
    else:
        return x.isnull().all().all()


def all_na(x):
    return x.isnull().all(axis=None)

