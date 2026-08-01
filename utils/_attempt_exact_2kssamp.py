
def _attempt_exact_2kssamp(n1, n2, g, d, alternative):
    """Attempts to compute the exact 2sample probability.

    n1, n2 are the sample sizes
    g is the gcd(n1, n2)
    d is the computed max difference in ECDFs

    Returns (success, d, probability)
    """
    lcm = (n1 // g) * n2
    h = int(np.round(d * lcm))
    d = h * 1.0 / lcm
    if h == 0:
        return True, d, 1.0
    saw_fp_error, prob = False, np.nan
    try:
        with np.errstate(invalid="raise", over="raise"):
            if alternative == 'two-sided':
                if n1 == n2:
                    prob = _compute_prob_outside_square(n1, h)
                else:
                    prob = _compute_outer_prob_inside_method(n1, n2, g, h)
            else:
                if n1 == n2:
                    # prob = binom(2n, n-h) / binom(2n, n)
                    # Evaluating in that form incurs roundoff errors
                    # from special.binom. Instead calculate directly
                    jrange = np.arange(h)
                    prob = np.prod((n1 - jrange) / (n1 + jrange + 1.0))
                else:
                    with np.errstate(over='raise'):
                        num_paths = _count_paths_outside_method(n1, n2, g, h)
                    bin = special.binom(n1 + n2, n1)
                    if num_paths > bin or np.isinf(bin):
                        saw_fp_error = True
                    else:
                        prob = num_paths / bin

    except (FloatingPointError, OverflowError):
        saw_fp_error = True

    if saw_fp_error:
        return False, d, np.nan
    if not (0 <= prob <= 1):
        return False, d, prob
    return True, d, prob

