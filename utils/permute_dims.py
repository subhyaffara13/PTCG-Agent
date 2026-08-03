import copy

def permute_dims(A, axes=None, copy=False):
    """Permute the axes of the sparse array `A` to the order `axes`.

    Parameters
    ----------
    A : sparse array
        Input array.
    axes : tuple or list of ints, optional
        If specified, it must be a tuple or list which contains a permutation
        of ``[0, 1, ..., N-1]`` where ``N`` is ``A.ndim``. The ith
        axis of the returned array will correspond to the axis numbered ``axes[i]``
        of the input. If not specified, defaults to ``range(A.ndim)[::-1]``,
        which reverses the order of the axes.
    copy : bool, optional (default: False)
        Whether to return the permutation as a copy. If False, an in-place
        permutation is provided if possible depending on format.

    Returns
    -------
    out : sparse array in COO format
        A copy of `A` with permuted axes.

    Raises
    ------
    ValueError
        If provided a non-integer or out of range ``[-N, N-1]`` axis,
        where ``N`` is ``A.ndim``.

    Examples
    --------
    >>> from scipy.sparse import coo_array, permute_dims
    >>> A = coo_array([[[1, 2, 3], [2, 0, 0]]])
    >>> A.shape
    (1, 2, 3)
    >>> permute_dims(A, axes=(1, 2, 0)).shape
    (2, 3, 1)

    """
    ndim = A.ndim
    if axes is None:
        axes = tuple(range(ndim)[::-1])
    elif len(axes) != ndim:
        raise ValueError(f"Incorrect number of axes: {ndim} instead of {A.ndim}")

    # -------------This is from _sputils.validateaxis which almost does what we want
    # TODO stop _sputils.validateaxis from returning `None` when len(axes)==ndim
    if not isinstance(axes, tuple | list):
        # If not a tuple, check that the provided axes is actually
        # an integer and raise a TypeError similar to NumPy's
        if not np.issubdtype(np.dtype(type(axes)), np.integer):
            raise TypeError(f'axis must be an integer/tuple of ints, not {type(axes)}')
        axes = (axes,)

    canon_axes = []
    for ax in axes:
        if not isintlike(ax):
            raise TypeError(f"axis must be an integer. (given {ax})")
        if ax < 0:
            ax += ndim
        if ax < 0 or ax >= ndim:
            raise ValueError("axis out of range for ndim")
        canon_axes.append(ax)

    if len(canon_axes) != len(set(canon_axes)):
        raise ValueError("duplicate value in axis")
    # -------------End of code from  _sputils.validateaxis
    axes = canon_axes
    if axes == list(range(ndim)):
        return A if not copy else A.copy()

    A = A.tocoo(copy=copy)
    A._shape = tuple(A.shape[idx] for idx in axes)
    A.coords = tuple(A.coords[idx] for idx in axes)
    A.has_canonical_format = False  # data usually no longer sorted
    return A


def permute_dims(x: Array, /, axes: tuple[int, ...], xp: Namespace) -> Array:
    return xp.transpose(x, axes)


def permute_dims(x: Array, /, axes: tuple[int, ...]) -> Array:
    return torch.permute(x, axes)


def permute_dims(a: ArrayLike, /, axes: tuple[int, ...]) -> Array:
  """Permute the axes/dimensions of an array.

  JAX implementation of :func:`array_api.permute_dims`.

  Args:
    a: input array
    axes: tuple of integers in range ``[0, a.ndim)`` specifying the
      axes permutation.

  Returns:
    a copy of ``a`` with axes permuted.

  See also:
    - :func:`jax.numpy.transpose`
    - :func:`jax.numpy.matrix_transpose`

  Examples:
    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.permute_dims(a, (1, 0))
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)
  """
  a = util.ensure_arraylike("permute_dims", a)
  return lax.transpose(a, axes)

