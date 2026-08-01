
def dsplit(ary: ArrayLike, indices_or_sections):
    if ary.ndim < 3:
        raise ValueError("dsplit only works on arrays of 3 or more dimensions")
    return _split_helper(ary, indices_or_sections, 2, strict=True)


def dsplit(a: TensorLikeType, sections: DimsType) -> TensorSequenceType:
    if a.ndim < 3:
        raise RuntimeError(
            f"torch.dsplit requires a tensor with at least 3 dimension, but got a tensor with {a.ndim} dimensions!"
        )
    # pyrefly: ignore [unsupported-operation]
    if isinstance(sections, IntLike) and (sections == 0 or a.shape[2] % sections != 0):
        raise RuntimeError(
            "torch.dsplit attempted to split along dimension 2, "
            + f"but the size of the dimension {a.shape[2]} is not divisible by the split_size {sections}!"
        )
    return tensor_split(a, sections, 2)


def dsplit(ary, indices_or_sections):
    """
    Split array into multiple sub-arrays along the 3rd axis (depth).

    Please refer to the `split` documentation.  `dsplit` is equivalent
    to `split` with ``axis=2``, the array is always split along the third
    axis provided the array dimension is greater than or equal to 3.

    See Also
    --------
    split : Split an array into multiple sub-arrays of equal size.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(16.0).reshape(2, 2, 4)
    >>> x
    array([[[ 0.,   1.,   2.,   3.],
            [ 4.,   5.,   6.,   7.]],
           [[ 8.,   9.,  10.,  11.],
            [12.,  13.,  14.,  15.]]])
    >>> np.dsplit(x, 2)
    [array([[[ 0.,  1.],
            [ 4.,  5.]],
           [[ 8.,  9.],
            [12., 13.]]]), array([[[ 2.,  3.],
            [ 6.,  7.]],
           [[10., 11.],
            [14., 15.]]])]
    >>> np.dsplit(x, np.array([3, 6]))
    [array([[[ 0.,   1.,   2.],
            [ 4.,   5.,   6.]],
           [[ 8.,   9.,  10.],
            [12.,  13.,  14.]]]),
     array([[[ 3.],
            [ 7.]],
           [[11.],
            [15.]]]),
    array([], shape=(2, 2, 0), dtype=float64)]
    """
    if _nx.ndim(ary) < 3:
        raise ValueError('dsplit only works on arrays of 3 or more dimensions')
    return split(ary, indices_or_sections, 2)


def dsplit(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
  """Split an array into sub-arrays depth-wise.

  JAX implementation of :func:`numpy.dsplit`.

  Refer to the documentation of :func:`jax.numpy.split` for details. ``dsplit`` is
  equivalent to ``split`` with ``axis=2``.

  Examples:

    >>> x = jnp.arange(12).reshape(3, 1, 4)
    >>> print(x)
    [[[ 0  1  2  3]]
    <BLANKLINE>
     [[ 4  5  6  7]]
    <BLANKLINE>
     [[ 8  9 10 11]]]
    >>> x1, x2 = jnp.dsplit(x, 2)
    >>> print(x1)
    [[[0 1]]
    <BLANKLINE>
     [[4 5]]
    <BLANKLINE>
     [[8 9]]]
    >>> print(x2)
    [[[ 2  3]]
    <BLANKLINE>
     [[ 6  7]]
    <BLANKLINE>
     [[10 11]]]

  See also:
    - :func:`jax.numpy.split`: split an array along any axis.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
  """
  return _split("dsplit", ary, indices_or_sections, axis=2)

