
def flip(image: Image.Image) -> Image.Image:
    """
    Flip the image vertically (top to bottom).

    :param image: The image to flip.
    :return: An image.
    """
    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)


def flip(func, a, b):
    """ Call the function call with the arguments flipped

    This function is curried.

    >>> def div(a, b):
    ...     return a // b
    ...
    >>> flip(div, 2, 6)
    3
    >>> div_by_two = flip(div, 2)
    >>> div_by_two(4)
    2

    This is particularly useful for built in functions and functions defined
    in C extensions that accept positional only arguments. For example:
    isinstance, issubclass.

    >>> data = [1, 'a', 'b', 2, 1.5, object(), 3]
    >>> only_ints = list(filter(flip(isinstance, int), data))
    >>> only_ints
    [1, 2, 3]
    """
    return func(b, a)


def flip(m: ArrayLike, axis=None):
    # XXX: semantic difference: np.flip returns a view, torch.flip copies
    if axis is None:
        axis = tuple(range(m.ndim))
    else:
        axis = _util.normalize_axis_tuple(axis, m.ndim)
    return torch.flip(m, axis)


def flip(a: TensorLikeType, dims: DimsSequenceType) -> TensorLikeType:
    if not isinstance(dims, tuple) and not isinstance(dims, list):
        raise ValueError("dims has to be a sequence of ints")
    dims = utils.canonicalize_dims(a.ndim, dims)  # type: ignore[assignment]
    utils.validate_no_repeating_dims(dims)
    return prims.rev(a, dims)


def flip(g: jit_utils.GraphContext, input, dims):
    return symbolic_helper._slice_helper(
        g,
        input,
        axes=dims,
        starts=[-1] * len(dims),
        ends=[-_constants.INT64_MAX] * len(dims),
        steps=[-1] * len(dims),
    )


def flip(x: Array, /, *, axis: int | tuple[int, ...] | None = None, **kwargs: object) -> Array:
    if axis is None:
        axis = tuple(range(x.ndim))
    # torch.flip doesn't accept dim as an int but the method does
    # https://github.com/pytorch/pytorch/issues/18095
    return x.flip(axis, **kwargs)


def flip(m, axis=None):
    """
    Reverse the order of elements in an array along the given axis.

    The shape of the array is preserved, but the elements are reordered.

    Parameters
    ----------
    m : array_like
        Input array.
    axis : None or int or tuple of ints, optional
         Axis or axes along which to flip over. The default,
         axis=None, will flip over all of the axes of the input array.
         If axis is negative it counts from the last to the first axis.

         If axis is a tuple of ints, flipping is performed on all of the axes
         specified in the tuple.

    Returns
    -------
    out : array_like
        A view of `m` with the entries of axis reversed.  Since a view is
        returned, this operation is done in constant time.

    See Also
    --------
    flipud : Flip an array vertically (axis=0).
    fliplr : Flip an array horizontally (axis=1).

    Notes
    -----
    flip(m, 0) is equivalent to flipud(m).

    flip(m, 1) is equivalent to fliplr(m).

    flip(m, n) corresponds to ``m[...,::-1,...]`` with ``::-1`` at position n.

    flip(m) corresponds to ``m[::-1,::-1,...,::-1]`` with ``::-1`` at all
    positions.

    flip(m, (0, 1)) corresponds to ``m[::-1,::-1,...]`` with ``::-1`` at
    position 0 and position 1.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.arange(8).reshape((2,2,2))
    >>> A
    array([[[0, 1],
            [2, 3]],
           [[4, 5],
            [6, 7]]])
    >>> np.flip(A, 0)
    array([[[4, 5],
            [6, 7]],
           [[0, 1],
            [2, 3]]])
    >>> np.flip(A, 1)
    array([[[2, 3],
            [0, 1]],
           [[6, 7],
            [4, 5]]])
    >>> np.flip(A)
    array([[[7, 6],
            [5, 4]],
           [[3, 2],
            [1, 0]]])
    >>> np.flip(A, (0, 2))
    array([[[5, 4],
            [7, 6]],
           [[1, 0],
            [3, 2]]])
    >>> rng = np.random.default_rng()
    >>> A = rng.normal(size=(3,4,5))
    >>> np.all(np.flip(A,2) == A[:,:,::-1,...])
    True
    """
    if not hasattr(m, 'ndim'):
        m = asarray(m)
    if axis is None:
        indexer = (np.s_[::-1],) * m.ndim
    else:
        axis = _nx.normalize_axis_tuple(axis, m.ndim)
        indexer = [np.s_[:]] * m.ndim
        for ax in axis:
            indexer[ax] = np.s_[::-1]
        indexer = tuple(indexer)
    return m[indexer]


def flip(m: ArrayLike, axis: int | Sequence[int] | None = None) -> Array:
  """Reverse the order of elements of an array along the given axis.

  JAX implementation of :func:`numpy.flip`.

  Args:
    m: Array.
    axis: integer or sequence of integers. Specifies along which axis or axes
      should the array elements be reversed. Default is ``None``, which flips
      along all axes.

  Returns:
    An array with the elements in reverse order along ``axis``.

  See Also:
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1 (left/right)
    - :func:`jax.numpy.flipud`: reverse the order along axis 0 (up/down)

  Examples:
    >>> x1 = jnp.array([[1, 2],
    ...                 [3, 4]])
    >>> jnp.flip(x1)
    Array([[4, 3],
           [2, 1]], dtype=int32)

    If ``axis`` is specified with an integer, then ``jax.numpy.flip`` reverses
    the array along that particular axis only.

    >>> jnp.flip(x1, axis=1)
    Array([[2, 1],
           [4, 3]], dtype=int32)

    >>> x2 = jnp.arange(1, 9).reshape(2, 2, 2)
    >>> x2
    Array([[[1, 2],
            [3, 4]],
    <BLANKLINE>
           [[5, 6],
            [7, 8]]], dtype=int32)
    >>> jnp.flip(x2)
    Array([[[8, 7],
            [6, 5]],
    <BLANKLINE>
           [[4, 3],
            [2, 1]]], dtype=int32)

    When ``axis`` is specified with a sequence of integers, then
    ``jax.numpy.flip`` reverses the array along the specified axes.

    >>> jnp.flip(x2, axis=[1, 2])
    Array([[[4, 3],
            [2, 1]],
    <BLANKLINE>
           [[8, 7],
            [6, 5]]], dtype=int32)
  """
  arr = util.ensure_arraylike("flip", m)
  return _flip(arr, reductions._ensure_optional_axes(axis))

