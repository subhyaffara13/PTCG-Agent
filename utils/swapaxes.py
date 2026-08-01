
def swapaxes(a: ArrayLike, axis1, axis2):
    axis1 = _util.normalize_axis_index(axis1, a.ndim)
    axis2 = _util.normalize_axis_index(axis2, a.ndim)
    return torch.swapaxes(a, axis1, axis2)


def swapaxes(A, axis1, axis2):
    """Interchange two axes of an array.

    Parameters
    ----------
    A : sparse array
        Input array.
    axis1 : int
        First axis.
    axis2 : int
        Second axis.

    Returns
    -------
    a_swapped : sparse array in COO format
        A copy of the input array with the two identified axes swapped.

    Raises
    ------
    ValueError
        If provided a non-integer or out of range ``[-N, N-1]`` axis,
        where ``N`` is ``A.ndim``.

    Examples
    --------
    >>> from scipy.sparse import coo_array, swapaxes
    >>> A = coo_array([[[1, 2, 3], [2, 0, 0]]])
    >>> A.shape
    (1, 2, 3)
    >>> swapaxes(A, 1, 2).shape
    (1, 3, 2)

    """
    axes = np.arange(A.ndim)
    try:
        axes[[axis1, axis2]] = axes[[axis2, axis1]]
    except IndexError as err:
        # original msg looks like: "index -4 is out of bounds for axis 0 with size 2"
        msg = str(err)
        msg = msg.removeprefix('index ').split(' axis ', 1)[0]
        # Final error is: "Invalid axis: -4 is out of bounds for ndim=2"
        raise ValueError(f"Invalid axis: {msg} ndim={A.ndim}")

    axes = tuple(axes)
    return permute_dims(A, axes=axes, copy=True)


def swapaxes(a, axis1, axis2):
    """
    Interchange two axes of an array.

    Parameters
    ----------
    a : array_like
        Input array.
    axis1 : int
        First axis.
    axis2 : int
        Second axis.

    Returns
    -------
    a_swapped : ndarray
        For NumPy >= 1.10.0, if `a` is an ndarray, then a view of `a` is
        returned; otherwise a new array is created. For earlier NumPy
        versions a view of `a` is returned only if the order of the
        axes is changed, otherwise the input array is returned.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[1,2,3]])
    >>> np.swapaxes(x,0,1)
    array([[1],
           [2],
           [3]])

    >>> x = np.array([[[0,1],[2,3]],[[4,5],[6,7]]])
    >>> x
    array([[[0, 1],
            [2, 3]],
           [[4, 5],
            [6, 7]]])

    >>> np.swapaxes(x,0,2)
    array([[[0, 4],
            [2, 6]],
           [[1, 5],
            [3, 7]]])

    """
    return _wrapfunc(a, 'swapaxes', axis1, axis2)


def swapaxes(a: ArrayLike, axis1: int, axis2: int) -> Array:
  """Swap two axes of an array.

  JAX implementation of :func:`numpy.swapaxes`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    axis1: index of first axis
    axis2: index of second axis

  Returns:
    Copy of ``a`` with specified axes swapped.

  Notes:
    Unlike :func:`numpy.swapaxes`, :func:`jax.numpy.swapaxes` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.moveaxis`: move a single axis of an array.
    - :func:`jax.numpy.rollaxis`: older API for ``moveaxis``.
    - :func:`jax.lax.transpose`: more general axes permutations.
    - :meth:`jax.Array.swapaxes`: same functionality via an array method.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))
    >>> jnp.swapaxes(a, 1, 3).shape
    (2, 5, 4, 3)

    Equivalent output via the ``swapaxes`` array method:

    >>> a.swapaxes(1, 3).shape
    (2, 5, 4, 3)

    Equivalent output via :func:`~jax.numpy.transpose`:

    >>> a.transpose(0, 3, 2, 1).shape
    (2, 5, 4, 3)
  """
  a = util.ensure_arraylike("swapaxes", a)
  perm = np.arange(np.ndim(a))
  perm[axis1], perm[axis2] = perm[axis2], perm[axis1]
  return lax.transpose(a, list(perm))

