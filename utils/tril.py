
def tril(m: ArrayLike, k=0):
    return torch.tril(m, k)


def tril(a: TensorLikeType, diagonal: int = 0) -> TensorLikeType:
    torch._check(
        a.ndim >= 2, lambda: "tril: input tensor must have at least 2 dimensions"
    )
    h, w = a.shape[-2:]
    mask = (
        torch.arange(w, device=a.device).unsqueeze(-2)
        - torch.arange(h, device=a.device).unsqueeze(-1)
    ) <= diagonal

    # aten.tril always returns a new contiguous tensor
    # contiguous() is needed to correctly model the output stride
    return utils.mask_tensor(mask, a).contiguous()


def tril(g: jit_utils.GraphContext, self, diagonal, out=None):
    return g.op("Trilu", self, diagonal, upper_i=0)


def tril(A, k=0, format=None):
    """Return the lower triangular portion of a sparse array or matrix.

    Returns the elements on or below the k-th diagonal of A.
        - k = 0 corresponds to the main diagonal
        - k > 0 is above the main diagonal
        - k < 0 is below the main diagonal

    .. warning::

        `tril` is switching to the sparse array interface.

        For the case where no input arrays are sparse, this function is
        switching to returning a sparse array instead of sparse matrix.
        Control the sparse return class by making at least one input sparse,
        e.g., ``tril(coo_matrix(A))``, or ``tril(coo_array(A))``.
        That removes any deprecation warnings as well.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        Handling of this no sparse input case will change no earlier than v1.20.

    Parameters
    ----------
    A : dense or sparse array or matrix
        Matrix whose lower trianglar portion is desired.
    k : int : optional
        The top-most diagonal of the lower triangle.
    format : str
        Sparse format of the result, e.g. format="csr", etc.

    Returns
    -------
    L : sparse matrix
        Lower triangular portion of A in sparse format.

    See Also
    --------
    triu : upper triangle in sparse format

    Examples
    --------
    >>> from scipy.sparse import csr_array, tril
    >>> A = csr_array([[1, 2, 0, 0, 3], [4, 5, 0, 6, 7], [0, 0, 8, 9, 0]],
    ...               dtype='int32')
    >>> A.toarray()
    array([[1, 2, 0, 0, 3],
           [4, 5, 0, 6, 7],
           [0, 0, 8, 9, 0]], dtype=int32)
    >>> tril(A).toarray()
    array([[1, 0, 0, 0, 0],
           [4, 5, 0, 0, 0],
           [0, 0, 8, 0, 0]], dtype=int32)
    >>> tril(A).nnz
    4
    >>> tril(A, k=1).toarray()
    array([[1, 2, 0, 0, 0],
           [4, 5, 0, 0, 0],
           [0, 0, 8, 9, 0]], dtype=int32)
    >>> tril(A, k=-1).toarray()
    array([[0, 0, 0, 0, 0],
           [4, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]], dtype=int32)
    >>> tril(A, format='csc')
    <Compressed Sparse Column sparse array of dtype 'int32'
        with 4 stored elements and shape (3, 5)>

    """
    if isinstance(A, sparray):
        coo_sparse = coo_array
    elif isinstance(A, spmatrix):
        coo_sparse = coo_matrix
    else:  # dense
        msg = """`tril` is switching to the sparse array interface.

        For the case where input arrays are numpy arrays, this function is
        switching to returning a sparse array instead of sparse matrix.
        Recover the sparse matrix return value by making one input a sparse matrix.
        For example, tril(coo_matrix(A)).
        Avoid this message for sparse array output by using tril(coo_array(A)).
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
    mask = A.row + k >= A.col

    row = A.row[mask]
    col = A.col[mask]
    data = A.data[mask]
    new_coo = coo_sparse((data, (row, col)), shape=A.shape, dtype=A.dtype)
    return new_coo.asformat(format)


def tril(x: Array, /, *, k: int = 0) -> Array:
    return torch.tril(x, k)


def tril(m, k=0):
    """
    Lower triangle of an array.

    Return a copy of an array with elements above the `k`-th diagonal zeroed.
    For arrays with ``ndim`` exceeding 2, `tril` will apply to the final two
    axes.

    Parameters
    ----------
    m : array_like, shape (..., M, N)
        Input array.
    k : int, optional
        Diagonal above which to zero elements.  `k = 0` (the default) is the
        main diagonal, `k < 0` is below it and `k > 0` is above.

    Returns
    -------
    tril : ndarray, shape (..., M, N)
        Lower triangle of `m`, of same shape and data-type as `m`.

    See Also
    --------
    triu : same thing, only for the upper triangle

    Examples
    --------
    >>> import numpy as np
    >>> np.tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
    array([[ 0,  0,  0],
           [ 4,  0,  0],
           [ 7,  8,  0],
           [10, 11, 12]])

    >>> np.tril(np.arange(3*4*5).reshape(3, 4, 5))
    array([[[ 0,  0,  0,  0,  0],
            [ 5,  6,  0,  0,  0],
            [10, 11, 12,  0,  0],
            [15, 16, 17, 18,  0]],
           [[20,  0,  0,  0,  0],
            [25, 26,  0,  0,  0],
            [30, 31, 32,  0,  0],
            [35, 36, 37, 38,  0]],
           [[40,  0,  0,  0,  0],
            [45, 46,  0,  0,  0],
            [50, 51, 52,  0,  0],
            [55, 56, 57, 58,  0]]])

    """
    m = asanyarray(m)
    mask = tri(*m.shape[-2:], k=k, dtype=bool)

    return where(mask, m, zeros(1, m.dtype))


def tril(m: ArrayLike, k: int = 0) -> Array:
  r"""Return lower triangle of an array.

  JAX implementation of :func:`numpy.tril`

  Args:
    m: input array. Must have ``m.ndim >= 2``.
    k: k: optional, int, default=0. Specifies the sub-diagonal above which the
      elements of the array are set to zero. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.

  Returns:
    An array with same shape as input containing the lower triangle of the given
    array with elements above the sub-diagonal specified by ``k`` are set to
    zero.

  See also:
    - :func:`jax.numpy.triu`: Returns an upper triangle of an array.
    - :func:`jax.numpy.tri`: Returns an array with ones on and below the
      diagonal and zeros elsewhere.

  Examples:
    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8],
    ...                [9, 10, 11, 12]])
    >>> jnp.tril(x)
    Array([[ 1,  0,  0,  0],
           [ 5,  6,  0,  0],
           [ 9, 10, 11,  0]], dtype=int32)
    >>> jnp.tril(x, k=1)
    Array([[ 1,  2,  0,  0],
           [ 5,  6,  7,  0],
           [ 9, 10, 11, 12]], dtype=int32)
    >>> jnp.tril(x, k=-1)
    Array([[ 0,  0,  0,  0],
           [ 5,  0,  0,  0],
           [ 9, 10,  0,  0]], dtype=int32)

    When ``m.ndim > 2``, ``jnp.tril`` operates batch-wise on the trailing axes.

    >>> x1 = jnp.array([[[1, 2],
    ...                  [3, 4]],
    ...                 [[5, 6],
    ...                  [7, 8]]])
    >>> jnp.tril(x1)
    Array([[[1, 0],
            [3, 4]],
    <BLANKLINE>
           [[5, 0],
            [7, 8]]], dtype=int32)
  """
  m = util.ensure_arraylike("tril", m)
  m_shape = np.shape(m)
  if len(m_shape) < 2:
    raise ValueError("Argument to jax.numpy.tril must be at least 2D")
  N, M = m_shape[-2:]
  mask = tri(N, M, k=k, dtype=bool)
  which = lax.broadcast(mask, m_shape[:-2], out_sharding=core.typeof(m).sharding)
  assert which.shape == m_shape
  return lax.select(which, m, array_creation.zeros_like(m))

