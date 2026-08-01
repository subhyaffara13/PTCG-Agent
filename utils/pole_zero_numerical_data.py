
def pole_zero_numerical_data(system):
    """
    Returns the numerical data of poles and zeros of the system.
    It is internally used by ``pole_zero_plot`` to get the data
    for plotting poles and zeros. Users can use this data to further
    analyse the dynamics of the system or plot using a different
    backend/plotting-module.

    Parameters
    ==========

    system : SISOLinearTimeInvariant
        The system for which the pole-zero data is to be computed.

    Returns
    =======

    tuple : (zeros, poles)
        zeros = Zeros of the system as a list of Python float/complex.
        poles = Poles of the system as a list of Python float/complex.

    Raises
    ======

    NotImplementedError
        When a SISO LTI system is not passed.

        When time delay terms are present in the system.

    ValueError
        When more than one free symbol is present in the system.
        The only variable in the transfer function should be
        the variable of the Laplace transform.

    Examples
    ========

    >>> from sympy.abc import s
    >>> from sympy.physics.control.lti import TransferFunction
    >>> from sympy.physics.control.control_plots import pole_zero_numerical_data
    >>> tf1 = TransferFunction(s**2 + 1, s**4 + 4*s**3 + 6*s**2 + 5*s + 2, s)
    >>> pole_zero_numerical_data(tf1)
    ([-1j, 1j], [-2.0, -1.0, (-0.5-0.8660254037844386j), (-0.5+0.8660254037844386j)])

    See Also
    ========

    pole_zero_plot

    """
    _check_system(system)
    system = system.doit()  # Get the equivalent TransferFunction object.

    num_poly = Poly(system.num, system.var)
    den_poly = Poly(system.den, system.var)

    return _poly_roots(num_poly), _poly_roots(den_poly)

