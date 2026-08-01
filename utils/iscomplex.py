
def iscomplex(x: ArrayLike):
    if torch.is_complex(x):
        return x.imag != 0
    return torch.zeros_like(x, dtype=torch.bool)


def iscomplex(var):
    return isscalar(var) and \
           var.get('typespec') in ['complex', 'double complex']


def iscomplex(x):
    """
    Returns a bool array, where True if input element is complex.

    What is tested is whether the input has a non-zero imaginary part, not if
    the input type is complex.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    out : ndarray of bools
        Output array.

    See Also
    --------
    isreal
    iscomplexobj : Return True if x is a complex type or an array of complex
                   numbers.

    Examples
    --------
    >>> import numpy as np
    >>> np.iscomplex([1+1j, 1+0j, 4.5, 3, 2, 2j])
    array([ True, False, False, False, False,  True])

    """
    ax = asanyarray(x)
    if issubclass(ax.dtype.type, _nx.complexfloating):
        return ax.imag != 0
    res = zeros(ax.shape, bool)
    return res[()]   # convert to scalar if needed


def iscomplex(x: ArrayLike) -> Array:
  """Return boolean array showing where the input is complex.

  JAX implementation of :func:`numpy.iscomplex`.

  Args:
    x: Input array to check.

  Returns:
    A new array containing boolean values indicating complex elements.

  See Also:
    - :func:`jax.numpy.iscomplexobj`
    - :func:`jax.numpy.isrealobj`

  Examples:
    >>> jnp.iscomplex(jnp.array([True, 0, 1, 2j, 1+2j]))
    Array([False, False, False, True, True], dtype=bool)
  """
  i = ufuncs.imag(x)
  return lax.ne(i, lax._const(i, 0))

