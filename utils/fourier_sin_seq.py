
def fourier_sin_seq(func, limits, n):
    """Returns the sin sequence in a Fourier series"""
    from sympy.integrals import integrate
    x, L = limits[0], limits[2] - limits[1]
    sin_term = sin(2*n*pi*x / L)
    return SeqFormula(2 * sin_term * integrate(func * sin_term, limits)
                      / L, (n, 1, oo))

