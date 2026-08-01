
def moveaxis(a: ArrayLike, source, destination):
    source = _util.normalize_axis_tuple(source, a.ndim, "source")
    destination = _util.normalize_axis_tuple(destination, a.ndim, "destination")
    return torch.moveaxis(a, source, destination)


def moveaxis(a, source, destination):
    """
    Move axes of an array to new positions.

    Other axes remain in their original order.

    Parameters
    ----------
    a : np.ndarray
        The array whose axes should be reordered.
    source : int or sequence of int
        Original positions of the axes to move. These must be unique.
    destination : int or sequence of int
        Destination positions for each of the original axes. These must also be
        unique.

    Returns
    -------
    result : np.ndarray
        Array with moved axes. This array is a view of the input array.

    See Also
    --------
    transpose : Permute the dimensions of an array.
    swapaxes : Interchange two axes of an array.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.zeros((3, 4, 5))
    >>> np.moveaxis(x, 0, -1).shape
    (4, 5, 3)
    >>> np.moveaxis(x, -1, 0).shape
    (5, 3, 4)

    These all achieve the same result:

    >>> np.transpose(x).shape
    (5, 4, 3)
    >>> np.swapaxes(x, 0, -1).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1], [-1, -2]).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1, 2], [-1, -2, -3]).shape
    (5, 4, 3)

    """
    try:
        # allow duck-array types if they define transpose
        transpose = a.transpose
    except AttributeError:
        a = asarray(a)
        transpose = a.transpose

    source = normalize_axis_tuple(source, a.ndim, 'source')
    destination = normalize_axis_tuple(destination, a.ndim, 'destination')
    if len(source) != len(destination):
        raise ValueError('`source` and `destination` arguments must have '
                         'the same number of elements')

    order = [n for n in range(a.ndim) if n not in source]

    for dest, src in sorted(zip(destination, source)):
        order.insert(dest, src)

    result = transpose(order)
    return result


def moveaxis(x: Array, src: int | Sequence[int], dst: int | Sequence[int]) -> Array:
  if src == dst:
    return x
  if isinstance(src, int):
    src = (src,)
  if isinstance(dst, int):
    dst = (dst,)
  src = [canonicalize_axis(a, x.ndim) for a in src]
  dst = [canonicalize_axis(a, x.ndim) for a in dst]
  perm = [i for i in range(np.ndim(x)) if i not in src]
  for d, s in sorted(zip(dst, src)):
    perm.insert(d, s)
  return x.transpose(perm)


def moveaxis(a: ArrayLike, source: int | Sequence[int],
             destination: int | Sequence[int]) -> Array:
  """Move an array axis to a new position

  JAX implementation of :func:`numpy.moveaxis`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    source: index or indices of the axes to move.
    destination: index or indices of the axes destinations

  Returns:
    Copy of ``a`` with axes moved from ``source`` to ``destination``.

  Notes:
    Unlike :func:`numpy.moveaxis`, :func:`jax.numpy.moveaxis` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize away
    such copies when possible, so this doesn't have performance impacts in practice.

  See also:
    - :func:`jax.numpy.swapaxes`: swap two axes.
    - :func:`jax.numpy.rollaxis`: older API for moving an axis.
    - :func:`jax.numpy.transpose`: general axes permutation.

  Examples:
    >>> a = jnp.ones((2, 3, 4, 5))

    Move axis ``1`` to the end of the array:

    >>> jnp.moveaxis(a, 1, -1).shape
    (2, 4, 5, 3)

    Move the last axis to position 1:

    >>> jnp.moveaxis(a, -1, 1).shape
    (2, 5, 3, 4)

    Move multiple axes:

    >>> jnp.moveaxis(a, (0, 1), (-1, -2)).shape
    (4, 5, 3, 2)

    This can also be accomplished via :func:`~jax.numpy.transpose`:

    >>> a.transpose(2, 3, 1, 0).shape
    (4, 5, 3, 2)
  """
  arr = util.ensure_arraylike("moveaxis", a)
  return _moveaxis(arr, _ensure_index_tuple(source),
                   _ensure_index_tuple(destination))

