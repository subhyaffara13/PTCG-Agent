
def broadcast_arrays(*args: ArrayLike, subok: NotImplementedType = False):
    return torch.broadcast_tensors(*args)


def broadcast_arrays(*arrays: Array) -> tuple[Array, ...]:
    return tuple(cp.broadcast_arrays(*arrays))


def broadcast_arrays(*arrays: Array) -> tuple[Array, ...]:
    shape = torch.broadcast_shapes(*[a.shape for a in arrays])
    return tuple(torch.broadcast_to(a, shape) for a in arrays)


def broadcast_arrays(*args, subok=False):
    """
    Broadcast any number of arrays against each other.

    Parameters
    ----------
    *args : array_likes
        The arrays to broadcast.

    subok : bool, optional
        If True, then sub-classes will be passed-through, otherwise
        the returned arrays will be forced to be a base-class array (default).

    Returns
    -------
    broadcasted : tuple of arrays
        These arrays are views on the original arrays.  They are typically
        not contiguous.  Furthermore, more than one element of a
        broadcasted array may refer to a single memory location. If you need
        to write to the arrays, make copies first. While you can set the
        ``writable`` flag True, writing to a single output value may end up
        changing more than one location in the output array.

        .. deprecated:: 1.17
            The output is currently marked so that if written to, a deprecation
            warning will be emitted. A future version will set the
            ``writable`` flag False so writing to it will raise an error.

    See Also
    --------
    broadcast
    broadcast_to
    broadcast_shapes

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[1,2,3]])
    >>> y = np.array([[4],[5]])
    >>> np.broadcast_arrays(x, y)
    (array([[1, 2, 3],
            [1, 2, 3]]),
     array([[4, 4, 4],
            [5, 5, 5]]))

    Here is a useful idiom for getting contiguous copies instead of
    non-contiguous views.

    >>> [np.array(a) for a in np.broadcast_arrays(x, y)]
    [array([[1, 2, 3],
            [1, 2, 3]]),
     array([[4, 4, 4],
            [5, 5, 5]])]

    """
    # nditer is not used here to avoid the limit of 64 arrays.
    # Otherwise, something like the following one-liner would suffice:
    # return np.nditer(args, flags=['multi_index', 'zerosize_ok'],
    #                  order='C').itviews

    args = [np.array(_m, copy=None, subok=subok) for _m in args]

    shape = _broadcast_shape(*args)

    result = [array if array.shape == shape
              else _broadcast_to(array, shape, subok=subok, readonly=False)
                              for array in args]
    return tuple(result)


def broadcast_arrays(*args: ArrayLike) -> list[Array]:
  """Broadcast arrays to a common shape.

  JAX implementation of :func:`numpy.broadcast_arrays`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    args: zero or more array-like objects to be broadcasted.

  Returns:
    a list of arrays containing broadcasted copies of the inputs.

  See also:
    - :func:`jax.numpy.broadcast_shapes`: broadcast input shapes to a common shape.
    - :func:`jax.numpy.broadcast_to`: broadcast an array to a specified shape.

  Examples:

    >>> x = jnp.arange(3)
    >>> y = jnp.int32(1)
    >>> jnp.broadcast_arrays(x, y)
    [Array([0, 1, 2], dtype=int32), Array([1, 1, 1], dtype=int32)]

    >>> x = jnp.array([[1, 2, 3]])
    >>> y = jnp.array([[10],
    ...                [20]])
    >>> x2, y2 = jnp.broadcast_arrays(x, y)
    >>> x2
    Array([[1, 2, 3],
           [1, 2, 3]], dtype=int32)
    >>> y2
    Array([[10, 10, 10],
           [20, 20, 20]], dtype=int32)

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  args = util.ensure_arraylike_tuple("broadcast_arrays", args)
  return util._broadcast_arrays(*args)

