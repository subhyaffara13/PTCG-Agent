
def eye(n, M=None, k=0, dtype=float, order='C'):
    """
    Return a matrix with ones on the diagonal and zeros elsewhere.

    Parameters
    ----------
    n : int
        Number of rows in the output.
    M : int, optional
        Number of columns in the output, defaults to `n`.
    k : int, optional
        Index of the diagonal: 0 refers to the main diagonal,
        a positive value refers to an upper diagonal,
        and a negative value to a lower diagonal.
    dtype : dtype, optional
        Data-type of the returned matrix.
    order : {'C', 'F'}, optional
        Whether the output should be stored in row-major (C-style) or
        column-major (Fortran-style) order in memory.

    Returns
    -------
    I : matrix
        A `n` x `M` matrix where all elements are equal to zero,
        except for the `k`-th diagonal, whose values are equal to one.

    See Also
    --------
    numpy.eye : Equivalent array function.
    identity : Square identity matrix.

    Examples
    --------
    >>> import numpy.matlib
    >>> np.matlib.eye(3, k=1, dtype=np.float64)
    matrix([[0.,  1.,  0.],
            [0.,  0.,  1.],
            [0.,  0.,  0.]])

    """
    return asmatrix(np.eye(n, M=M, k=k, dtype=dtype, order=order))


def eye(
    N,
    M=None,
    k=0,
    dtype: DTypeLike | None = None,
    order: NotImplementedType = "C",
    *,
    like: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.default_dtypes().float_dtype
    if M is None:
        M = N
    z = torch.zeros(N, M, dtype=dtype)
    z.diagonal(k).fill_(1)
    return z


def eye(
    n: int,
    m: int | None = None,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
    requires_grad: bool = False,  # TODO: unused
) -> TensorLikeType:
    """
    Reference implementation of torch.eye
    """
    if m is None:
        m = n

    torch._check(n >= 0, lambda: f"n must be greater or equal to 0, got {n}")
    torch._check(m >= 0, lambda: f"m must be greater or equal to 0, got {m}")

    range_dtype = torch.int64
    if isinstance(n, utils.IntWithoutSymInt) and isinstance(m, utils.IntWithoutSymInt):
        range_dtype = _strength_reduce_integer(max(n, m))
    range_n = torch.arange(n, dtype=range_dtype, device=device, requires_grad=False)
    range_m = torch.arange(m, dtype=range_dtype, device=device, requires_grad=False)

    cond = range_n.unsqueeze(-1) == range_m
    if layout in (torch.strided, None) and not pin_memory:
        return cond.to(dtype or torch.get_default_dtype())
    else:
        one = torch.ones(
            (1,),
            dtype=dtype,
            layout=layout,
            device=device,
            pin_memory=pin_memory,
            requires_grad=False,
        )
        return torch.where(cond, one, 0)


def eye(g: jit_utils.GraphContext, *args):
    if len(args) == 5:
        # aten::eye(n, dtype, layout, device, pin_memory)
        n, dtype, layout, device, _pin_memory = args
        dim_size = symbolic_helper._unsqueeze_helper(g, n, [0])
        shape = g.op("Concat", dim_size, dim_size, axis_i=0)
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)
    if len(args) == 6:
        # aten::eye(n, m, dtype, layout, device, pin_memory)
        n, m, dtype, layout, device, _pin_memory = args
        shape = g.op(
            "Concat",
            symbolic_helper._unsqueeze_helper(g, n, [0]),
            symbolic_helper._unsqueeze_helper(g, m, [0]),
            axis_i=0,
        )
        tensor = zeros(g, shape, dtype, layout, device)
        return g.op("EyeLike", tensor)

    return symbolic_helper._unimplemented("aten::eye", f"with {len(args)} arguments")


def eye(*args, **kwargs):
    """Create square identity matrix n x n

    See Also
    ========

    diag
    zeros
    ones
    """

    return Matrix.eye(*args, **kwargs)


def eye(m, n=None, k=0, dtype=float, format=None):
    """Sparse matrix of chosen shape with ones on the kth diagonal and zeros elsewhere.

    Returns a sparse matrix (m x n) where the kth diagonal
    is all ones and everything else is zeros.

    .. warning::

        This function returns a sparse matrix -- not a sparse array.
        You are encouraged to use `eye_array` to take advantage
        of the sparse array functionality.

    Parameters
    ----------
    m : int
        Number of rows in the matrix.
    n : int, optional
        Number of columns. Default: `m`.
    k : int, optional
        Diagonal to place ones on. Default: 0 (main diagonal).
    dtype : dtype, optional
        Data type of the matrix.
    format : str, optional
        Sparse format of the result, e.g., format="csr", etc.

    Returns
    -------
    new_matrix : sparse matrix
        Sparse matrix of chosen shape with ones on the kth diagonaland zeros elsewhere.

    See Also
    --------
    eye_array : Sparse array of chosen shape with ones on a specified diagonal.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy as sp
    >>> sp.sparse.eye(3).toarray()
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    >>> sp.sparse.eye(3, dtype=np.int8)
    <DIAgonal sparse matrix of dtype 'int8'
        with 3 stored elements (1 diagonals) and shape (3, 3)>

    """
    return _eye(m, n, k, dtype, format, False)


def eye(
    n_rows: int,
    n_cols: int | None = None,
    /,
    *,
    xp: Namespace,
    k: int = 0,
    dtype: DType | None = None,
    device: Device | None = None,
    **kwargs: object,
) -> Array:
    _check_device(xp, device)
    return xp.eye(n_rows, M=n_cols, k=k, dtype=dtype, **kwargs)


def eye(n_rows: int,
        n_cols: int | None = None,
        /,
        *,
        k: int = 0,
        dtype: DType | None = None,
        device: Device | None = None,
        **kwargs: object) -> Array:
    if n_cols is None:
        n_cols = n_rows
    z = torch.zeros(n_rows, n_cols, dtype=dtype, device=device, **kwargs)
    if abs(k) <= n_rows + n_cols:
        z.diagonal(k).fill_(1)
    return z


def eye(N, M=None, k=0, dtype=float, order='C', *, device=None, like=None):
    """
    Return a 2-D array with ones on the diagonal and zeros elsewhere.

    Parameters
    ----------
    N : int
      Number of rows in the output.
    M : int, optional
      Number of columns in the output. If None, defaults to `N`.
    k : int, optional
      Index of the diagonal: 0 (the default) refers to the main diagonal,
      a positive value refers to an upper diagonal, and a negative value
      to a lower diagonal.
    dtype : data-type, optional
      Data-type of the returned array.
    order : {'C', 'F'}, optional
        Whether the output should be stored in row-major (C-style) or
        column-major (Fortran-style) order in memory.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    I : ndarray of shape (N,M)
      An array where all elements are equal to zero, except for the `k`-th
      diagonal, whose values are equal to one.

    See Also
    --------
    identity : (almost) equivalent function
    diag : diagonal 2-D array from a 1-D array specified by the user.

    Examples
    --------
    >>> import numpy as np
    >>> np.eye(2, dtype=np.int_)
    array([[1, 0],
           [0, 1]])
    >>> np.eye(3, k=1)
    array([[0.,  1.,  0.],
           [0.,  0.,  1.],
           [0.,  0.,  0.]])

    """
    if like is not None:
        return _eye_with_like(
            like, N, M=M, k=k, dtype=dtype, order=order, device=device
        )
    if M is None:
        M = N
    m = zeros((N, M), dtype=dtype, order=order, device=device)
    if k >= M:
        return m
    # Ensure M and k are integers, so we don't get any surprise casting
    # results in the expressions `M-k` and `M+1` used below.  This avoids
    # a problem with inputs with type (for example) np.uint64.
    M = operator.index(M)
    k = operator.index(k)
    if k >= 0:
        i = k
    else:
        i = (-k) * M
    m[:M - k].flat[i::M + 1] = 1
    return m


def eye(N: DimSize, M: DimSize | None = None,
        k: int | ArrayLike = 0,
        dtype: DTypeLike | None = None,
        *, device: xc.Device | Sharding | None = None) -> Array:
  """Create a square or rectangular identity matrix

  JAX implementation of :func:`numpy.eye`.

  Args:
    N: integer specifying the first dimension of the array.
    M: optional integer specifying the second dimension of the array;
      defaults to the same value as ``N``.
    k: optional integer specifying the offset of the diagonal. Use positive
      values for upper diagonals, and negative values for lower diagonals.
      Default is zero.
    dtype: optional dtype; defaults to floating point.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Identity array of shape ``(N, M)``, or ``(N, N)`` if ``M`` is not specified.

  See also:
    :func:`jax.numpy.identity`: Simpler API for generating square identity matrices.

  Examples:
    A simple 3x3 identity matrix:

    >>> jnp.eye(3)
    Array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]], dtype=float32)

    Integer identity matrices with offset diagonals:

    >>> jnp.eye(3, k=1, dtype=int)
    Array([[0, 1, 0],
           [0, 0, 1],
           [0, 0, 0]], dtype=int32)
    >>> jnp.eye(3, k=-1, dtype=int)
    Array([[0, 0, 0],
           [1, 0, 0],
           [0, 1, 0]], dtype=int32)

    Non-square identity matrix:

    >>> jnp.eye(3, 5, k=1)
    Array([[0., 1., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 1., 0.]], dtype=float32)
  """
  # TODO(vfdev-5): optimize putting the array directly on the device specified
  # instead of putting it on default device and then on the specific device
  output = _eye(N, M=M, k=k, dtype=dtype)
  if device is not None:
    return api.device_put(output, device=device)
  return output


def eye(N: int, M: int | None = None, k: int = 0, dtype: DTypeLike | None = None,
        index_dtype: DTypeLike = 'int32', sparse_format: str = 'bcoo', **kwds) -> JAXSparse:
  """Create 2D sparse identity matrix.

  Args:
    N: int. Number of rows in the output.
    M: int, optional. Number of columns in the output. If None, defaults to `N`.
    k: int, optional. Index of the diagonal: 0 (the default) refers to the main
       diagonal, a positive value refers to an upper diagonal, and a negative value
       to a lower diagonal.
    dtype: data-type, optional. Data-type of the returned array.
    index_dtype: (optional) dtype of the index arrays.
    format: string specifying the matrix format (e.g. ['bcoo']).
    **kwds: additional keywords passed to the format-specific _empty constructor.

  Returns:
    I: two-dimensional sparse matrix with ones along the k-th diagonal.
  """
  formats = {'bcoo': BCOO, 'coo': COO, 'csr': CSR, 'csc': CSC}
  if M is None:
    M = N
  N = core.concrete_or_error(operator.index, N)
  M = core.concrete_or_error(operator.index, M)
  k = core.concrete_or_error(operator.index, k)

  cls = formats[sparse_format]
  return cls._eye(M=M, N=N, k=k, dtype=dtype, index_dtype=index_dtype, **kwds)

