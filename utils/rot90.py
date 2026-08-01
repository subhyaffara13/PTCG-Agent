
def rot90(m: ArrayLike, k=1, axes=(0, 1)):
    axes = _util.normalize_axis_tuple(axes, m.ndim)
    return torch.rot90(m, k, axes)


def rot90(
    a: TensorLikeType, k: int = 1, dims: DimsSequenceType = (0, 1)
) -> TensorLikeType:
    """Reference implementation of :func:`torch.rot90`."""
    if len(dims) != 2:
        raise RuntimeError(
            f"expected total rotation dims == 2, but got dims = {len(dims)}"
        )
    if a.ndim < 2:
        raise RuntimeError(f"expected total dims >= 2, but got total dims = {a.ndim}")

    # Do this after the initial checks to be compatible with the behavior in
    # core.
    dims = utils.canonicalize_dims(a.ndim, dims)

    if dims[0] == dims[1]:
        raise RuntimeError(
            f"expected rotation dims to be different, but got dim0 = {dims[0]} and dim1 = {dims[1]}"
        )
    k = k % 4  # Rotation direction is from the second towards the first axis for k < 0
    if k == 1:
        return torch.transpose(torch.flip(a, (dims[1],)), dims[0], dims[1])
    elif k == 2:
        return torch.flip(a, dims)
    elif k == 3:
        return torch.transpose(torch.flip(a, (dims[0],)), dims[0], dims[1])
    else:
        return a.clone(memory_format=torch.contiguous_format)


def rot90(m, k=1, axes=(0, 1)):
    """
    Rotate an array by 90 degrees in the plane specified by axes.

    Rotation direction is from the first towards the second axis.
    This means for a 2D array with the default `k` and `axes`, the
    rotation will be counterclockwise.

    Parameters
    ----------
    m : array_like
        Array of two or more dimensions.
    k : integer
        Number of times the array is rotated by 90 degrees.
    axes : (2,) array_like
        The array is rotated in the plane defined by the axes.
        Axes must be different.

    Returns
    -------
    y : ndarray
        A rotated view of `m`.

    See Also
    --------
    flip : Reverse the order of elements in an array along the given axis.
    fliplr : Flip an array horizontally.
    flipud : Flip an array vertically.

    Notes
    -----
    ``rot90(m, k=1, axes=(1,0))``  is the reverse of
    ``rot90(m, k=1, axes=(0,1))``

    ``rot90(m, k=1, axes=(1,0))`` is equivalent to
    ``rot90(m, k=-1, axes=(0,1))``

    Examples
    --------
    >>> import numpy as np
    >>> m = np.array([[1,2],[3,4]], int)
    >>> m
    array([[1, 2],
           [3, 4]])
    >>> np.rot90(m)
    array([[2, 4],
           [1, 3]])
    >>> np.rot90(m, 2)
    array([[4, 3],
           [2, 1]])
    >>> m = np.arange(8).reshape((2,2,2))
    >>> np.rot90(m, 1, (1,2))
    array([[[1, 3],
            [0, 2]],
           [[5, 7],
            [4, 6]]])

    """
    axes = tuple(axes)
    if len(axes) != 2:
        raise ValueError("len(axes) must be 2.")

    m = asanyarray(m)

    if axes[0] == axes[1] or absolute(axes[0] - axes[1]) == m.ndim:
        raise ValueError("Axes must be different.")

    if (axes[0] >= m.ndim or axes[0] < -m.ndim
        or axes[1] >= m.ndim or axes[1] < -m.ndim):
        raise ValueError(f"Axes={axes} out of range for array of ndim={m.ndim}.")

    try:
        k = operator.index(k)
    except TypeError:
        # DEPRECATED 2026-04-27, NumPy 2.5
        msg = (f"Passing a value for k ({k!r}) that is not an integer type has been "
               "deprecated in NumPy 2.5. The value will be cast to an integer.  In "
               "the future this will be an error.")
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        k = int(k)

    k %= 4

    if k == 0:
        return m[:]
    if k == 2:
        return flip(flip(m, axes[0]), axes[1])

    axes_list = arange(0, m.ndim)
    (axes_list[axes[0]], axes_list[axes[1]]) = (axes_list[axes[1]],
                                                axes_list[axes[0]])

    if k == 1:
        return transpose(flip(m, axes[1]), axes_list)
    else:
        # k == 3
        return flip(transpose(m, axes_list), axes[1])


def rot90(m: ArrayLike, k: int = 1, axes: tuple[int, int] = (0, 1)) -> Array:
  """Rotate an array by 90 degrees counterclockwise in the plane specified by axes.

  JAX implementation of :func:`numpy.rot90`.

  Args:
    m: input array. Must have ``m.ndim >= 2``.
    k: int, optional, default=1. Specifies the number of times the array is rotated.
      For negative values of ``k``, the array is rotated in clockwise direction.
    axes: tuple of 2 integers, optional, default= (0, 1). The axes define the plane
      in which the array is rotated. Both the axes must be different.

  Returns:
    An array containing the copy of the input, ``m`` rotated by 90 degrees.

  See also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1 (left/right)
    - :func:`jax.numpy.flipud`: reverse the order along axis 0 (up/down)

  Examples:
    >>> m = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.rot90(m)
    Array([[3, 6],
           [2, 5],
           [1, 4]], dtype=int32)
    >>> jnp.rot90(m, k=2)
    Array([[6, 5, 4],
           [3, 2, 1]], dtype=int32)

    ``jnp.rot90(m, k=1, axes=(1, 0))`` is equivalent to
    ``jnp.rot90(m, k=-1, axes(0,1))``.

    >>> jnp.rot90(m, axes=(1, 0))
    Array([[4, 1],
           [5, 2],
           [6, 3]], dtype=int32)
    >>> jnp.rot90(m, k=-1, axes=(0, 1))
    Array([[4, 1],
           [5, 2],
           [6, 3]], dtype=int32)

    when input array has ``ndim>2``:

    >>> m1 = jnp.array([[[1, 2, 3],
    ...                  [4, 5, 6]],
    ...                 [[7, 8, 9],
    ...                  [10, 11, 12]]])
    >>> jnp.rot90(m1, k=1, axes=(2, 1))
    Array([[[ 4,  1],
            [ 5,  2],
            [ 6,  3]],
    <BLANKLINE>
           [[10,  7],
            [11,  8],
            [12,  9]]], dtype=int32)
  """
  m = util.ensure_arraylike("rot90", m)
  if np.ndim(m) < 2:
    raise ValueError("rot90 requires its first argument to have ndim at least "
                     f"two, but got first argument of shape {np.shape(m)}, "
                     f"which has ndim {np.ndim(m)}")
  ax1, ax2 = axes
  ax1 = _canonicalize_axis(ax1, np.ndim(m))
  ax2 = _canonicalize_axis(ax2, np.ndim(m))
  if ax1 == ax2:
    raise ValueError("Axes must be different")  # same as numpy error
  k = k % 4
  if k == 0:
    return asarray(m)
  elif k == 2:
    return flip(flip(m, ax1), ax2)
  else:
    perm = list(range(np.ndim(m)))
    perm[ax1], perm[ax2] = perm[ax2], perm[ax1]
    if k == 1:
      return transpose(flip(m, ax2), perm)
    else:
      return flip(transpose(m, perm), ax2)

