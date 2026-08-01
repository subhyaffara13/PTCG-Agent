
def hyperfocal_distance(f, N, c):
    """

    Parameters
    ==========

    f: sympifiable
        Focal length of a given lens.

    N: sympifiable
        F-number of a given lens.

    c: sympifiable
        Circle of Confusion (CoC) of a given image format.

    Example
    =======

    >>> from sympy.physics.optics import hyperfocal_distance
    >>> round(hyperfocal_distance(f = 0.5, N = 8, c = 0.0033), 2)
    9.47
    """

    f = sympify(f)
    N = sympify(N)
    c = sympify(c)

    return (1/(N * c))*(f**2)

