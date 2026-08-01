
def reflective_filter(R):
    """A reflective filter Jones matrix with reflectance ``R``.

    Parameters
    ==========

    R : numeric type or SymPy Symbol
        The reflectance of the filter.

    Returns
    =======

    SymPy Matrix
        A Jones matrix representing the filter.

    Examples
    ========

    A generic filter.

    >>> from sympy import pprint, symbols
    >>> from sympy.physics.optics.polarization import reflective_filter
    >>> R = symbols("R", real=True)
    >>> pprint(reflective_filter(R), use_unicode=True)
    ⎡√R   0 ⎤
    ⎢       ⎥
    ⎣0   -√R⎦

    """
    return Matrix([[sqrt(R), 0], [0, -sqrt(R)]])

