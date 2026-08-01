
def _chatterjeexi_iv(y_continuous, method):
    # Input validation for `chatterjeexi`
    # x, y, `axis` input validation taken care of by decorator

    if y_continuous not in {True, False}:
        raise ValueError('`y_continuous` must be boolean.')

    if not isinstance(method, stats.PermutationMethod):
        method = method.lower()
        message = "`method` must be 'asymptotic' or a `PermutationMethod` instance."
        if method != 'asymptotic':
            raise ValueError(message)

    return y_continuous, method

