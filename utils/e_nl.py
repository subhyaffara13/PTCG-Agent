
def E_nl(n, Z=1):
    """
    Returns the energy of the state (n, l) in Hartree atomic units.

    The energy does not depend on "l".

    Parameters
    ==========

    n : integer
        Principal Quantum Number which is
        an integer with possible values as 1, 2, 3, 4,...
    Z :
        Atomic number (1 for Hydrogen, 2 for Helium, ...)

    Examples
    ========

    >>> from sympy.physics.hydrogen import E_nl
    >>> from sympy.abc import n, Z
    >>> E_nl(n, Z)
    -Z**2/(2*n**2)
    >>> E_nl(1)
    -1/2
    >>> E_nl(2)
    -1/8
    >>> E_nl(3)
    -1/18
    >>> E_nl(3, 47)
    -2209/18

    """
    n, Z = S(n), S(Z)
    if n.is_integer and (n < 1):
        raise ValueError("'n' must be positive integer")
    return -Z**2/(2*n**2)


def E_nl(n, l, hw):
    """
    Returns the Energy of an isotropic harmonic oscillator.

    Parameters
    ==========

    n :
        The "nodal" quantum number.
    l :
        The orbital angular momentum.
    hw :
        The harmonic oscillator parameter.

    Notes
    =====

    The unit of the returned value matches the unit of hw, since the energy is
    calculated as:

        E_nl = (2*n + l + 3/2)*hw

    Examples
    ========

    >>> from sympy.physics.sho import E_nl
    >>> from sympy import symbols
    >>> x, y, z = symbols('x, y, z')
    >>> E_nl(x, y, z)
    z*(2*x + y + 3/2)
    """
    return (2*n + l + Rational(3, 2))*hw

