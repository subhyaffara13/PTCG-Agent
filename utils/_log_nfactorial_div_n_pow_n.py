
def _log_nfactorial_div_n_pow_n(n):
    # Computes n! / n**n
    #    = (n-1)! / n**(n-1)
    # Uses Stirling's approximation, but removes n*log(n) up-front to
    # avoid subtractive cancellation.
    #    = log(n)/2 - n + log(sqrt(2pi)) + sum B_{2j}/(2j)/(2j-1)/n**(2j-1)
    rn = 1.0/n
    return np.log(n)/2 - n + _LOG_2PI/2 + rn * np.polyval(_STIRLING_COEFFS, rn/n)

