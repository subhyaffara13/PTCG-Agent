
def _poisson_means_test_iv(k1, n1, k2, n2, diff, alternative):
    # """check for valid types and values of input to `poisson_mean_test`."""
    if k1 != int(k1) or k2 != int(k2):
        raise TypeError('`k1` and `k2` must be integers.')

    count_err = '`k1` and `k2` must be greater than or equal to 0.'
    if k1 < 0 or k2 < 0:
        raise ValueError(count_err)

    if n1 <= 0 or n2 <= 0:
        raise ValueError('`n1` and `n2` must be greater than 0.')

    if diff < 0:
        raise ValueError('diff must be greater than or equal to 0.')

    alternatives = {'two-sided', 'less', 'greater'}
    if alternative.lower() not in alternatives:
        raise ValueError(f"Alternative must be one of '{alternatives}'.")

