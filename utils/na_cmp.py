
def na_cmp():
    """
    Binary operator for comparing NA values.

    Should return a function of two arguments that returns
    True if both arguments are (scalar) NA for your type.

    By default, uses ``operator.is_``
    """
    return operator.is_


def na_cmp():
    def cmp(a, b):
        return a is pd.NaT and a is b

    return cmp


def na_cmp():
    # we are pd.NA
    return lambda x, y: x is pd.NA and y is pd.NA


def na_cmp():
    def cmp(a, b):
        return np.isnan(a) and np.isnan(b)

    return cmp


def na_cmp():
    return lambda left, right: pd.isna(left) and pd.isna(right)


def na_cmp():
    return lambda x, y: x.is_nan() and y.is_nan()


def na_cmp():
    return operator.eq

