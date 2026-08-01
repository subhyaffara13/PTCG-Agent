
def linear_polarizer(theta=0):
    """A linear polarizer Jones matrix with transmission axis at
    an angle ``theta``.

    Parameters
    ==========

    theta : numeric type or SymPy Symbol
        The angle of the transmission axis relative to the horizontal plane.

    Returns
    =======

    SymPy Matrix
        A Jones matrix representing the polarizer.

    Examples
    ========

    A generic polarizer.

    >>> from sympy import pprint, symbols
    >>> from sympy.physics.optics.polarization import linear_polarizer
    >>> theta = symbols("theta", real=True)
    >>> J = linear_polarizer(theta)
    >>> pprint(J, use_unicode=True)
    ⎡      2                     ⎤
    ⎢   cos (θ)     sin(θ)⋅cos(θ)⎥
    ⎢                            ⎥
    ⎢                     2      ⎥
    ⎣sin(θ)⋅cos(θ)     sin (θ)   ⎦


    """
    M = Matrix([[cos(theta)**2, sin(theta)*cos(theta)],
                [sin(theta)*cos(theta), sin(theta)**2]])
    return M

