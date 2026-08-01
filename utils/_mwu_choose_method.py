
def _mwu_choose_method(n1, n2, ties):
    """Choose method 'asymptotic' or 'exact' depending on input size, ties"""

    # if both inputs are large, asymptotic is OK
    if n1 > 8 and n2 > 8:
        return "asymptotic"

    # if there are any ties, asymptotic is preferred
    if ties:
        return "asymptotic"

    return "exact"

