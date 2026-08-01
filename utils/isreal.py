
def isreal(x: ArrayLike):
    if torch.is_complex(x):
        return x.imag == 0
    return torch.ones_like(x, dtype=torch.bool)


def isreal(a: TensorLikeType) -> TensorLikeType:
    if utils.is_complex_dtype(a.dtype):
        return torch.imag(a) == 0
    return torch.ones_like(a, dtype=torch.bool)


def isreal(var):
    return isscalar(var) and var.get('typespec') == 'real'


def isreal(x):
    """
    Returns a bool array, where True if input element is real.

    If element has complex type with zero imaginary part, the return value
    for that element is True.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    out : ndarray, bool
        Boolean array of same shape as `x`.

    Notes
    -----
    `isreal` may behave unexpectedly for string or object arrays (see examples)

    See Also
    --------
    iscomplex
    isrealobj : Return True if x is not a complex type.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1+1j, 1+0j, 4.5, 3, 2, 2j], dtype=np.complex128)
    >>> np.isreal(a)
    array([False,  True,  True,  True,  True, False])

    The function does not work on string arrays.

    >>> a = np.array([2j, "a"], dtype=np.str_)
    >>> np.isreal(a)  # returns the result of `"" == 0` currently.
    array([False, False])

    Returns True for all elements that either have no ``.imag`` attribute
    or for which that attribute is zero:

    >>> a = np.array([1, "2", 3+4j], dtype=np.object_)
    >>> np.isreal(a)
    array([ True,  True,  False])

    """
    return imag(x) == 0


def isreal(x: ArrayLike) -> Array:
  """Return boolean array showing where the input is real.

  JAX implementation of :func:`numpy.isreal`.

  Args:
    x: input array to check.

  Returns:
    A new array containing boolean values indicating real elements.

  See Also:
    - :func:`jax.numpy.iscomplex`
    - :func:`jax.numpy.isrealobj`

  Examples:
    >>> jnp.isreal(jnp.array([False, 0j, 1, 2.1, 1+2j]))
    Array([ True,  True,  True,  True, False], dtype=bool)
  """
  i = ufuncs.imag(x)
  return lax.eq(i, lax._const(i, 0))

