
def vsplit(ary: ArrayLike, indices_or_sections):
    if ary.ndim < 2:
        raise ValueError("vsplit only works on arrays of 2 or more dimensions")
    return _split_helper(ary, indices_or_sections, 0, strict=True)


def vsplit(
    a: TensorLikeType, indices_or_sections: DimsType
) -> tuple[TensorLikeType, ...]:
    torch._check(
        a.ndim >= 2,
        lambda: (
            "torch.vsplit requires a tensor with at least 2 dimension, but got a tensor with "
            + str(a.ndim)
            + " dimensions!"
        ),
    )
    if isinstance(indices_or_sections, IntLike):
        split_size = indices_or_sections
        torch._check(
            # pyrefly: ignore [unsupported-operation]
            (split_size != 0 and a.shape[0] % split_size == 0),
            lambda: (
                f"torch.vsplit attempted to split along dimension 0"
                f", but the size of the dimension "
                f"{a.shape[0]}"
                f" is not divisible by the split_size "
                f"{split_size}"
                f"!"
            ),
        )

        return tensor_split(a, split_size, 0)

    torch._check_type(
        isinstance(indices_or_sections, (list, tuple)),
        lambda: (
            "vsplit(): received an invalid combination of arguments. "
            "Expected indices_or_sections to be of type int, list of ints or tuple of ints "
            f"but got type {type(indices_or_sections)}"
        ),
    )

    split_sizes = indices_or_sections
    return tensor_split(a, split_sizes, 0)


def vsplit(ary, indices_or_sections):
    """
    Split an array into multiple sub-arrays vertically (row-wise).

    Please refer to the ``split`` documentation.  ``vsplit`` is equivalent
    to ``split`` with `axis=0` (default), the array is always split along the
    first axis regardless of the array dimension.

    See Also
    --------
    split : Split an array into multiple sub-arrays of equal size.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(16.0).reshape(4, 4)
    >>> x
    array([[ 0.,   1.,   2.,   3.],
           [ 4.,   5.,   6.,   7.],
           [ 8.,   9.,  10.,  11.],
           [12.,  13.,  14.,  15.]])
    >>> np.vsplit(x, 2)
    [array([[0., 1., 2., 3.],
            [4., 5., 6., 7.]]),
     array([[ 8.,  9., 10., 11.],
            [12., 13., 14., 15.]])]
    >>> np.vsplit(x, np.array([3, 6]))
    [array([[ 0.,  1.,  2.,  3.],
            [ 4.,  5.,  6.,  7.],
            [ 8.,  9., 10., 11.]]),
     array([[12., 13., 14., 15.]]),
     array([], shape=(0, 4), dtype=float64)]

    With a higher dimensional array the split is still along the first axis.

    >>> x = np.arange(8.0).reshape(2, 2, 2)
    >>> x
    array([[[0.,  1.],
            [2.,  3.]],
           [[4.,  5.],
            [6.,  7.]]])
    >>> np.vsplit(x, 2)
    [array([[[0., 1.],
             [2., 3.]]]),
     array([[[4., 5.],
             [6., 7.]]])]

    """
    if _nx.ndim(ary) < 2:
        raise ValueError('vsplit only works on arrays of 2 or more dimensions')
    return split(ary, indices_or_sections, 0)


def vsplit(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
  """Split an array into sub-arrays vertically.

  JAX implementation of :func:`numpy.vsplit`.

  Refer to the documentation of :func:`jax.numpy.split` for details; ``vsplit`` is
  equivalent to ``split`` with ``axis=0``.

  Examples:
    1D array:

    >>> x = jnp.array([1, 2, 3, 4, 5, 6])
    >>> x1, x2 = jnp.vsplit(x, 2)
    >>> print(x1, x2)
    [1 2 3] [4 5 6]

    2D array:

    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8]])
    >>> x1, x2 = jnp.vsplit(x, 2)
    >>> print(x1, x2)
    [[1 2 3 4]] [[5 6 7 8]]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
  """
  return _split("vsplit", ary, indices_or_sections, axis=0)

