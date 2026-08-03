import math


def _norm_factor(p, k):
    """
    Numerically find frequency shift to apply to delay-normalized filter such
    that -3 dB point is at 1 rad/sec.

    `p` is an array_like of polynomial poles
    `k` is a float gain

    First 10 values are listed in "Bessel Scale Factors" table,
    "Bessel Filters Polynomials, Poles and Circuit Elements 2003, C. Bond."
    """
    p = np.asarray(p, dtype=np.complex128)

    def G(w):
        """
        Gain of filter
        """
        return np.abs(k / np.prod(1j*w - p))

    def cutoff(w):
        """
        When gain = -3 dB, return 0
        """
        return G(w) - 1/math.sqrt(2)

    return optimize.newton(cutoff, 1.5)

