
def factorial2(n, exact=False, extend="zero"):
    """
    Double factorial.

    This is the factorial with every second value skipped.  E.g., ``7!! = 7 * 5
    * 3 * 1``.  It can be approximated numerically as::

      n!! = 2 ** (n / 2) * gamma(n / 2 + 1) * sqrt(2 / pi)  n odd
          = 2 ** (n / 2) * gamma(n / 2 + 1)                 n even
          = 2 ** (n / 2) * (n / 2)!                         n even

    The formula for odd ``n`` is the basis for the complex extension.

    Parameters
    ----------
    n : int or float or complex (or array_like thereof)
        Input values for ``n!!``. Non-integer values require ``extend='complex'``.
        By default, the return value for ``n < 0`` is 0.
    exact : bool, optional
        If ``exact`` is set to True, calculate the answer exactly using
        integer arithmetic, otherwise use above approximation (faster,
        but yields floats instead of integers).
        Default is False.
    extend : str, optional
        One of ``'zero'`` or ``'complex'``; this determines how values ``n<0``
        are handled - by default they are 0, but it is possible to opt into the
        complex extension of the double factorial. This also enables passing
        complex values to ``n``.

        .. warning::

           Using the ``'complex'`` extension also changes the values of the
           double factorial for even integers, reducing them by a factor of
           ``sqrt(2/pi) ~= 0.79``, see [1].

    Returns
    -------
    nf : int or float or complex or ndarray
        Double factorial of ``n``, as integer, float or complex (depending on
        ``exact`` and ``extend``). Array inputs are returned as arrays.

    References
    ----------
    .. [1] Complex extension to double factorial
            https://en.wikipedia.org/wiki/Double_factorial#Complex_arguments

    Examples
    --------
    >>> from scipy.special import factorial2
    >>> factorial2(7, exact=False)
    np.float64(105.00000000000001)
    >>> factorial2(7, exact=True)
    105
    """
    return _factorialx_wrapper("factorial2", n, k=2, exact=exact, extend=extend)

