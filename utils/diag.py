
def diag(v: ArrayLike, k=0):
    return torch.diag(v, k)


def diag(
    self: TensorLikeType,
    offset: int = 0,
) -> TensorLikeType:
    ndim = self.dim()
    torch._check(
        ndim in (1, 2), lambda: f"diag(): Supports 1D or 2D tensors. Got {ndim}D"
    )
    if ndim == 1:
        return torch.diag_embed(self, offset)
    else:
        return torch.diagonal_copy(self, offset)


def diag(*values, strict=True, unpack=False, **kwargs):
    """Returns a matrix with the provided values placed on the
    diagonal. If non-square matrices are included, they will
    produce a block-diagonal matrix.

    Examples
    ========

    This version of diag is a thin wrapper to Matrix.diag that differs
    in that it treats all lists like matrices -- even when a single list
    is given. If this is not desired, either put a `*` before the list or
    set `unpack=True`.

    >>> from sympy import diag

    >>> diag([1, 2, 3], unpack=True)  # = diag(1,2,3) or diag(*[1,2,3])
    Matrix([
    [1, 0, 0],
    [0, 2, 0],
    [0, 0, 3]])

    >>> diag([1, 2, 3])  # a column vector
    Matrix([
    [1],
    [2],
    [3]])

    See Also
    ========
    .matrixbase.MatrixBase.eye
    .matrixbase.MatrixBase.diagonal
    .matrixbase.MatrixBase.diag
    .expressions.blockmatrix.BlockMatrix
    """
    return Matrix.diag(*values, strict=strict, unpack=unpack, **kwargs)


def diag(v, k=0):
    """
    Extract a diagonal or construct a diagonal array.

    See the more detailed documentation for ``numpy.diagonal`` if you use this
    function to extract a diagonal and wish to write to the resulting array;
    whether it returns a copy or a view depends on what version of numpy you
    are using.

    Parameters
    ----------
    v : array_like
        If `v` is a 2-D array, return a copy of its `k`-th diagonal.
        If `v` is a 1-D array, return a 2-D array with `v` on the `k`-th
        diagonal.
    k : int, optional
        Diagonal in question. The default is 0. Use `k>0` for diagonals
        above the main diagonal, and `k<0` for diagonals below the main
        diagonal.

    Returns
    -------
    out : ndarray
        The extracted diagonal or constructed diagonal array.

    See Also
    --------
    diagonal : Return specified diagonals.
    diagflat : Create a 2-D array with the flattened input as a diagonal.
    trace : Sum along diagonals.
    triu : Upper triangle of an array.
    tril : Lower triangle of an array.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(9).reshape((3,3))
    >>> x
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])

    >>> np.diag(x)
    array([0, 4, 8])
    >>> np.diag(x, k=1)
    array([1, 5])
    >>> np.diag(x, k=-1)
    array([3, 7])

    >>> np.diag(np.diag(x))
    array([[0, 0, 0],
           [0, 4, 0],
           [0, 0, 8]])

    """
    v = asanyarray(v)
    s = v.shape
    if len(s) == 1:
        n = s[0] + abs(k)
        res = zeros((n, n), v.dtype)
        if k >= 0:
            i = k
        else:
            i = (-k) * n
        res[:n - k].flat[i::n + 1] = v
        return res
    elif len(s) == 2:
        return diagonal(v, k)
    else:
        raise ValueError("Input must be 1- or 2-d.")


def diag(v, k=0):
    """
    Extract a diagonal or construct a diagonal array.

    This function is the equivalent of `numpy.diag` that takes masked
    values into account, see `numpy.diag` for details.

    See Also
    --------
    numpy.diag : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np

    Create an array with negative values masked:

    >>> import numpy as np
    >>> x = np.array([[11.2, -3.973, 18], [0.801, -1.41, 12], [7, 33, -12]])
    >>> masked_x = np.ma.masked_array(x, mask=x < 0)
    >>> masked_x
    masked_array(
      data=[[11.2, --, 18.0],
            [0.801, --, 12.0],
            [7.0, 33.0, --]],
      mask=[[False,  True, False],
            [False,  True, False],
            [False, False,  True]],
      fill_value=1e+20)

    Isolate the main diagonal from the masked array:

    >>> np.ma.diag(masked_x)
    masked_array(data=[11.2, --, --],
                 mask=[False,  True,  True],
           fill_value=1e+20)

    Isolate the first diagonal below the main diagonal:

    >>> np.ma.diag(masked_x, -1)
    masked_array(data=[0.801, 33.0],
                 mask=[False, False],
           fill_value=1e+20)

    """
    output = np.diag(v, k).view(MaskedArray)
    if getmask(v) is not nomask:
        output._mask = np.diag(v._mask, k)
    return output


def diag(v: ArrayLike, k: int = 0) -> Array:
  """Returns the specified diagonal or constructs a diagonal array.

  JAX implementation of :func:`numpy.diag`.

  The JAX version always returns a copy of the input, although if this is used
  within a JIT compilation, the compiler may avoid the copy.

  Args:
    v: Input array. Can be a 1-D array to create a diagonal matrix or a
      2-D array to extract a diagonal.
    k: optional, default=0. Diagonal offset. Positive values place the diagonal
      above the main diagonal, negative values place it below the main diagonal.

  Returns:
    If `v` is a 2-D array, a 1-D array containing the diagonal elements.
    If `v` is a 1-D array, a 2-D array with the input elements placed along the
    specified diagonal.

  See also:
    - :func:`jax.numpy.diagflat`
    - :func:`jax.numpy.diagonal`

  Examples:
    Creating a diagonal matrix from a 1-D array:

    >>> jnp.diag(jnp.array([1, 2, 3]))
    Array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]], dtype=int32)

    Specifying a diagonal offset:

    >>> jnp.diag(jnp.array([1, 2, 3]), k=1)
    Array([[0, 1, 0, 0],
           [0, 0, 2, 0],
           [0, 0, 0, 3],
           [0, 0, 0, 0]], dtype=int32)

    Extracting a diagonal from a 2-D array:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.diag(x)
    Array([1, 5, 9], dtype=int32)
  """
  v = util.ensure_arraylike("diag", v)
  return _diag(v, operator.index(k))

