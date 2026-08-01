
def comb(N, k, *, exact=False, repetition=False):
    """The number of combinations of N things taken k at a time.

    This is often expressed as "N choose k".

    Parameters
    ----------
    N : int, ndarray
        Number of things.
    k : int, ndarray
        Number of elements taken.
    exact : bool, optional
        For integers, if `exact` is False, then floating point precision is
        used, otherwise the result is computed exactly.
    repetition : bool, optional
        If `repetition` is True, then the number of combinations with
        repetition is computed.

    Returns
    -------
    val : int, float, ndarray
        The total number of combinations.

    See Also
    --------
    binom : Binomial coefficient considered as a function of two real
            variables.

    Notes
    -----
    - Array arguments accepted only for exact=False case.
    - If N < 0, or k < 0, then 0 is returned.
    - If k > N and repetition=False, then 0 is returned.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import comb
    >>> k = np.array([3, 4])
    >>> n = np.array([10, 10])
    >>> comb(n, k, exact=False)
    array([ 120.,  210.])
    >>> comb(10, 3, exact=True)
    120
    >>> comb(10, 3, exact=True, repetition=True)
    220

    """
    if repetition:
        # Special case: C(n, 0) with repetition = 1 for n >= 0
        # Without this check, comb(0, 0, repetition=True) would compute
        # comb(-1, 0) which incorrectly returns 0
        if exact:
            if k == 0 and int(N) == N and N >= 0:
                return 1
        else:
            k, N = asarray(k), asarray(N)
            cond = (k == 0) & (N >= 0)
            vals = binom(N + k - 1, k)
            if isinstance(vals, np.ndarray):
                vals[cond] = 1.0
            elif cond:
                vals = np.float64(1.0)
            return vals
        return comb(N + k - 1, k, exact=exact)
    if exact:
        if int(N) == N and int(k) == k:
            # _comb_int casts inputs to integers, which is safe & intended here
            return _comb_int(N, k)
        else:
            raise ValueError("Non-integer `N` and `k` with `exact=True` is not "
                             "supported.")
    else:
        k, N = asarray(k), asarray(N)
        cond = (k <= N) & (N >= 0) & (k >= 0)
        vals = binom(N, k)
        if isinstance(vals, np.ndarray):
            vals[~cond] = 0
        elif not cond:
            vals = np.float64(0)
        return vals


def comb(N: ArrayLike, k: ArrayLike, *, repetition: bool = False) -> Array:
  r"""The number of combinations of N things taken k at a time ("N choose k").

  JAX implementation of :func:`scipy.special.comb`.

  .. math::

    \mathrm{comb}(N, k) = \binom{N}{k} = \frac{N!}{k!\,(N - k)!}

  Args:
    N: arraylike, number of things.
    k: arraylike, number of elements taken.
    repetition: bool, compute the number of combinations with repetition.

  Returns:
    array containing the total number of combinations.

  Notes:
    This computes the float-valued binomial coefficient via the
    :func:`~jax.scipy.special.gammaln` function. The ``exact`` argument
    from :func:`scipy.special.comb` is not supported because JAX does not
    support arbitrary-precision integers. If ``N < 0``, ``k < 0``, or
    ``k > N`` and ``repetition=False``, then 0 is returned.

  See Also:
    - :func:`jax.scipy.special.factorial`
    - :func:`jax.scipy.special.gammaln`
  """
  N, k = promote_args_inexact("comb", N, k)

  if repetition:
    cond = (k == 0) & (N >= 0)
    result = comb(N + k - 1, k, repetition=False)
    return jnp.where(cond, 1.0, result)

  cond = (k <= N) & (N >= 0) & (k >= 0)
  safe_N = jnp.where(cond, N, 0.0)
  safe_k = jnp.where(cond, k, 0.0)
  result = lax.exp(gammaln(safe_N + 1) - gammaln(safe_k + 1) - gammaln(safe_N + 1 - safe_k))
  return jnp.where(cond, result, 0.0)

