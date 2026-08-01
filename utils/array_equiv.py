
def array_equiv(a1: ArrayLike, a2: ArrayLike):
    # *almost* the same as array_equal: _equiv tries to broadcast, _equal does not
    try:
        a1_t, a2_t = torch.broadcast_tensors(a1, a2)
    except RuntimeError:
        # failed to broadcast => not equivalent
        return False
    return _tensor_equal(a1_t, a2_t)


def array_equiv(a1, a2):
    """
    Returns True if input arrays are shape consistent and all elements equal.

    Shape consistent means they are either the same shape, or one input array
    can be broadcasted to create the same shape as the other one.

    Parameters
    ----------
    a1, a2 : array_like
        Input arrays.

    Returns
    -------
    out : bool
        True if equivalent, False otherwise.

    Examples
    --------
    >>> import numpy as np
    >>> np.array_equiv([1, 2], [1, 2])
    True
    >>> np.array_equiv([1, 2], [1, 3])
    False

    Showing the shape equivalence:

    >>> np.array_equiv([1, 2], [[1, 2], [1, 2]])
    True
    >>> np.array_equiv([1, 2], [[1, 2, 1, 2], [1, 2, 1, 2]])
    False

    >>> np.array_equiv([1, 2], [[1, 2], [1, 3]])
    False

    """
    try:
        a1, a2 = asarray(a1), asarray(a2)
    except Exception:
        return False
    try:
        multiarray.broadcast(a1, a2)
    except Exception:
        return False

    return builtins.bool(asanyarray(a1 == a2).all())


def array_equiv(a1: ArrayLike, a2: ArrayLike) -> Array:
  """Check if two arrays are element-wise equal.

  JAX implementation of :func:`numpy.array_equiv`.

  This function will return ``False`` if the input arrays cannot be broadcasted
  to the same shape.

  Args:
    a1: first input array to compare.
    a2: second input array to compare.

  Returns:
    Boolean scalar array indicating whether the input arrays are
    element-wise equal after broadcasting.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.array_equal`

  Examples:
    >>> jnp.array_equiv(jnp.array([1, 2, 3]), jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
    >>> jnp.array_equiv(jnp.array([1, 2, 3]), jnp.array([1, 2, 4]))
    Array(False, dtype=bool)
    >>> jnp.array_equiv(jnp.array([[1, 2, 3], [1, 2, 3]]),
    ...                 jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
  """
  a1, a2 = asarray(a1), asarray(a2)
  try:
    eq = ufuncs.equal(a1, a2)
  except ValueError:
    # shapes are not broadcastable
    return array(False)
  return reductions.all(eq)

