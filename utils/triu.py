
def triu(m: ArrayLike, k=0):
    return torch.triu(m, k)


def triu(a: TensorLikeType, diagonal: int = 0) -> TensorLikeType:
    torch._check(
        a.ndim >= 2, lambda: "triu: input tensor must have at least 2 dimensions"
    )
    h, w = a.shape[-2:]
    mask = (
        torch.arange(w, device=a.device).unsqueeze(-2)
        - torch.arange(h, device=a.device).unsqueeze(-1)
    ) >= diagonal

    # aten.triu always returns a new contiguous tensor
    # contiguous() is needed to correctly model the output stride
    return utils.mask_tensor(mask, a).contiguous()


def triu(g: jit_utils.GraphContext, self, diagonal, out=None):
    return g.op("Trilu", self, diagonal, upper_i=1)


def triu(A, k=0, format=None):
    """Return the upper triangular portion of a sparse array or matrix.

    Returns the elements on or above the k-th diagonal of A.
        - k = 0 corresponds to the main diagonal
        - k > 0 is above the main diagonal
        - k < 0 is below the main diagonal

    .. warning::

        `triu` is switching to the sparse array interface.

        For the case where no input arrays are sparse, this function is
        switching to returning a sparse array instead of sparse matrix.
        Control the sparse return class by making at least one input sparse,
        e.g., ``triu(coo_matrix(A))``, or ``triu(coo_array(A))``.
        That removes any deprecation warnings as well.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        Handling of this no sparse input case will change no earlier than v1.20.

    Parameters
    ----------
    A : dense or sparse array or matrix
        Matrix whose upper trianglar portion is desired.
    k : int : optional
        The bottom-most diagonal of the upper triangle.
    format : str
        Sparse format of the result, e.g. format="csr", etc.

    Returns
    -------
    L : sparse array or matrix
        Upper triangular portion of A in sparse format.
        Sparse array if A is a sparse array, otherwise matrix.

    See Also
    --------
    tril : lower triangle in sparse format

    Examples
    --------
    >>> from scipy.sparse import csr_array, triu
    >>> A = csr_array([[1, 2, 0, 0, 3], [4, 5, 0, 6, 7], [0, 0, 8, 9, 0]],
    ...                dtype='int32')
    >>> A.toarray()
    array([[1, 2, 0, 0, 3],
           [4, 5, 0, 6, 7],
           [0, 0, 8, 9, 0]], dtype=int32)
    >>> triu(A).toarray()
    array([[1, 2, 0, 0, 3],
           [0, 5, 0, 6, 7],
           [0, 0, 8, 9, 0]], dtype=int32)
    >>> triu(A).nnz
    8
    >>> triu(A, k=1).toarray()
    array([[0, 2, 0, 0, 3],
           [0, 0, 0, 6, 7],
           [0, 0, 0, 9, 0]], dtype=int32)
    >>> triu(A, k=-1).toarray()
    array([[1, 2, 0, 0, 3],
           [4, 5, 0, 6, 7],
           [0, 0, 8, 9, 0]], dtype=int32)
    >>> triu(A, format='csc')
    <Compressed Sparse Column sparse array of dtype 'int32'
        with 8 stored elements and shape (3, 5)>

    """
    if isinstance(A, sparray):
        coo_sparse = coo_array
    elif isinstance(A, spmatrix):
        coo_sparse = coo_matrix
    else:  # dense
        msg = """`triu` is switching to the sparse array interface.

        For the case where input arrays are numpy arrays, this function is
        switching to returning a sparse array instead of sparse matrix.
        Recover the sparse matrix return value by making one input a sparse matrix.
        For example, triu(coo_matrix(A)).
        Avoid this message for sparse array output by using triu(coo_array(A)).
        For more information, see the spmatrix to sparray migration guide
        https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html

        This function will be changed no earlier than v1.20.
        """
        prefixes = (os.path.dirname(__file__),)
        warn(msg, category=DeprecationWarning, skip_file_prefixes=prefixes)
        # default when input is ndarray
        coo_sparse = coo_matrix

    # convert to COOrdinate format where things are easy
    A = coo_sparse(A, copy=False)
    mask = A.row + k <= A.col

    row = A.row[mask]
    col = A.col[mask]
    data = A.data[mask]
    new_coo = coo_sparse((data, (row, col)), shape=A.shape, dtype=A.dtype)
    return new_coo.asformat(format)


def triu(x: Array, /, *, k: int = 0) -> Array:
    return torch.triu(x, k)


def triu(m, k=0):
    """
    Upper triangle of an array.

    Return a copy of an array with the elements below the `k`-th diagonal
    zeroed. For arrays with ``ndim`` exceeding 2, `triu` will apply to the
    final two axes.

    Please refer to the documentation for `tril` for further details.

    See Also
    --------
    tril : lower triangle of an array

    Examples
    --------
    >>> import numpy as np
    >>> np.triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]])

    >>> np.triu(np.arange(3*4*5).reshape(3, 4, 5))
    array([[[ 0,  1,  2,  3,  4],
            [ 0,  6,  7,  8,  9],
            [ 0,  0, 12, 13, 14],
            [ 0,  0,  0, 18, 19]],
           [[20, 21, 22, 23, 24],
            [ 0, 26, 27, 28, 29],
            [ 0,  0, 32, 33, 34],
            [ 0,  0,  0, 38, 39]],
           [[40, 41, 42, 43, 44],
            [ 0, 46, 47, 48, 49],
            [ 0,  0, 52, 53, 54],
            [ 0,  0,  0, 58, 59]]])

    """
    m = asanyarray(m)
    mask = tri(*m.shape[-2:], k=k - 1, dtype=bool)

    return where(mask, zeros(1, m.dtype), m)


def triu(m: ArrayLike, k: int = 0) -> Array:
  r"""Return upper triangle of an array.

  JAX implementation of :func:`numpy.triu`

  Args:
    m: input array. Must have ``m.ndim >= 2``.
    k: optional, int, default=0. Specifies the sub-diagonal below which the
      elements of the array are set to zero. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.

  Returns:
    An array with same shape as input containing the upper triangle of the given
    array with elements below the sub-diagonal specified by ``k`` are set to
    zero.

  See also:
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array.
    - :func:`jax.numpy.tri`: Returns an array with ones on and below the
      diagonal and zeros elsewhere.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9],
    ...                [10, 11, 12]])
    >>> jnp.triu(x)
    Array([[1, 2, 3],
           [0, 5, 6],
           [0, 0, 9],
           [0, 0, 0]], dtype=int32)
    >>> jnp.triu(x, k=1)
    Array([[0, 2, 3],
           [0, 0, 6],
           [0, 0, 0],
           [0, 0, 0]], dtype=int32)
    >>> jnp.triu(x, k=-1)
    Array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]], dtype=int32)

    When ``m.ndim > 2``, ``jnp.triu`` operates batch-wise on the trailing axes.

    >>> x1 = jnp.array([[[1, 2],
    ...                  [3, 4]],
    ...                 [[5, 6],
    ...                  [7, 8]]])
    >>> jnp.triu(x1)
    Array([[[1, 2],
            [0, 4]],
    <BLANKLINE>
           [[5, 6],
            [0, 8]]], dtype=int32)
  """
  m = util.ensure_arraylike("triu", m)
  m_shape = np.shape(m)
  if len(m_shape) < 2:
    raise ValueError("Argument to jax.numpy.triu must be at least 2D")
  N, M = m_shape[-2:]
  mask = tri(N, M, k=k - 1, dtype=bool)
  which = lax.broadcast(mask, m_shape[:-2], out_sharding=core.typeof(m).sharding)
  assert which.shape == m_shape
  return lax.select(which, array_creation.zeros_like(m), m)

