
def factorial(x):
    return gamma(x+1.0)


def factorial(x):
    """Return x!."""
    return int(mlib.ifac(int(x)))


def factorial(n, exact=False, extend="zero"):
    """
    The factorial of a number or array of numbers.

    The factorial of non-negative integer `n` is the product of all
    positive integers less than or equal to `n`::

        n! = n * (n - 1) * (n - 2) * ... * 1

    Parameters
    ----------
    n : int or float or complex (or array_like thereof)
        Input values for ``n!``. Complex values require ``extend='complex'``.
        By default, the return value for ``n < 0`` is 0.
    exact : bool, optional
        If ``exact`` is set to True, calculate the answer exactly using
        integer arithmetic, otherwise approximate using the gamma function
        (faster, but yields floats instead of integers).
        Default is False.
    extend : str, optional
        One of ``'zero'`` or ``'complex'``; this determines how values ``n<0``
        are handled - by default they are 0, but it is possible to opt into the
        complex extension of the factorial (see below).

    Returns
    -------
    nf : int or float or complex or ndarray
        Factorial of ``n``, as integer, float or complex (depending on ``exact``
        and ``extend``). Array inputs are returned as arrays.

    Notes
    -----
    For arrays with ``exact=True``, the factorial is computed only once, for
    the largest input, with each other result computed in the process.
    The output dtype is increased to ``int64`` or ``object`` if necessary.

    With ``exact=False`` the factorial is approximated using the gamma
    function (which is also the definition of the complex extension):

    .. math:: n! = \\Gamma(n+1)

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import factorial
    >>> arr = np.array([3, 4, 5])
    >>> factorial(arr, exact=False)
    array([   6.,   24.,  120.])
    >>> factorial(arr, exact=True)
    array([  6,  24, 120])
    >>> factorial(5, exact=True)
    120

    """
    return _factorialx_wrapper("factorial", n, k=1, exact=exact, extend=extend)


def factorial(n: ArrayLike, exact: bool = False) -> Array:
  r"""Factorial function

  JAX implementation of :obj:`scipy.special.factorial`

  .. math::

     \mathrm{factorial}(n) = n! = \prod_{k=1}^n k

  Args:
    n: arraylike, values for which factorial will be computed elementwise
    exact: bool, only ``exact=False`` is supported.

  Returns:
    array containing values of the factorial.

  Notes:
    This computes the float-valued factorial via the :func:`~jax.scipy.special.gamma`
    function. JAX does not support exact factorials, because it is not particularly
    useful: above ``n=20``, the exact result cannot be represented by 64-bit integers,
    which are the largest integers available to JAX.

  See Also:
    :func:`jax.scipy.special.gamma`
  """
  if exact:
    raise NotImplementedError("factorial with exact=True")
  n, = promote_args_inexact("factorial", n)
  return jnp.where(n < 0, 0, lax.exp(lax.lgamma(n + 1)))

