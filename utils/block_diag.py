import os

def block_diag(*tensors):
    """Create a block diagonal matrix from provided tensors.

    Args:
        *tensors: One or more tensors with 0, 1, or 2 dimensions.

    Returns:
        Tensor: A 2 dimensional tensor with all the input tensors arranged in
        order such that their upper left and lower right corners are
        diagonally adjacent. All other elements are set to 0.

    Example::

        >>> import torch
        >>> A = torch.tensor([[0, 1], [1, 0]])
        >>> B = torch.tensor([[3, 4, 5], [6, 7, 8]])
        >>> C = torch.tensor(7)
        >>> D = torch.tensor([1, 2, 3])
        >>> E = torch.tensor([[4], [5], [6]])
        >>> torch.block_diag(A, B, C, D, E)
        tensor([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 4, 5, 0, 0, 0, 0, 0],
                [0, 0, 6, 7, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 2, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 6]])
    """
    # This wrapper exists to support variadic args.
    if has_torch_function(tensors):
        return handle_torch_function(block_diag, tensors, *tensors)
    return torch._C._VariableFunctions.block_diag(tensors)  # type: ignore[attr-defined]


def block_diag(*tensors: list[TensorLikeType]) -> TensorLikeType:
    """
    This is used as an input to PythonRefInfo. `torch.block_diag`
    expects arguments splatted, but `aten.block_diag` expects only
    one argument that is a list of Tensors.
    """
    return _block_diag_iterable(tensors)  # type: ignore[arg-type]


def block_diag(*arrs):
    """
    Create a block diagonal array from provided arrays.

    For example, given 2-D inputs `A`, `B` and `C`, the output will have these
    arrays arranged on the diagonal::

        [[A, 0, 0],
         [0, B, 0],
         [0, 0, C]]

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    *arrs : array_like
        Input arrays ``A, B, C, ...``. A 1-D array or array_like sequence of length
        ``n`` is treated as a 2-D array with shape ``(1, n)``.

    Returns
    -------
    D : ndarray
        Array with `A`, `B`, `C`, ... on the diagonal of the last two
        dimensions. `D` has the same dtype as the result type of the
        inputs.

    Notes
    -----
    If all the input arrays are square, the output is known as a
    block diagonal matrix.

    Empty sequences (i.e., array-likes of zero size) will not be ignored.
    Noteworthy, both ``[]`` and ``[[]]`` are treated as matrices with shape
    ``(1,0)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import block_diag
    >>> A = [[1, 0],
    ...      [0, 1]]
    >>> B = [[3, 4, 5],
    ...      [6, 7, 8]]
    >>> C = [[7]]
    >>> P = np.zeros((2, 0), dtype='int32')
    >>> block_diag(A, B, C)
    array([[1, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 0, 3, 4, 5, 0],
           [0, 0, 6, 7, 8, 0],
           [0, 0, 0, 0, 0, 7]])
    >>> block_diag(A, P, B, C)
    array([[1, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 3, 4, 5, 0],
           [0, 0, 6, 7, 8, 0],
           [0, 0, 0, 0, 0, 7]])
    >>> block_diag(1.0, [2, 3], [[4, 5], [6, 7]])
    array([[ 1.,  0.,  0.,  0.,  0.],
           [ 0.,  2.,  3.,  0.,  0.],
           [ 0.,  0.,  0.,  4.,  5.],
           [ 0.,  0.,  0.,  6.,  7.]])

    """
    xp = array_namespace(*arrs)

    if arrs == ():
        arrs = ([],)
    arrs = [xpx.atleast_nd(xp.asarray(a), ndim=2) for a in arrs]

    batch_shapes = [a.shape[:-2] for a in arrs]
    batch_shape = np.broadcast_shapes(*batch_shapes)
    arrs = [xp.broadcast_to(a, batch_shape + a.shape[-2:]) for a in arrs]
    out_dtype = xp.result_type(*arrs)
    block_shapes = [a.shape[-2:] for a in arrs]
    out = xp.zeros(batch_shape +
                   tuple(map(int, xp.sum(xp.asarray(block_shapes), axis=0))),
                   dtype=out_dtype)

    r, c = 0, 0
    for i, (rr, cc) in enumerate(block_shapes):
        out = xpx.at(out)[..., r:r+rr, c:c+cc].set(arrs[i])
        r += rr
        c += cc
    return out


def block_diag(mats, format=None, dtype=None):
    """
    Build a block diagonal sparse matrix or array from provided matrices.

    .. warning::

        `block_diag` is switching to the sparse array interface.

        For the case where no input arrays are sparse, this function is
        switching to returning a sparse array instead of sparse matrix.
        Control the sparse return class by making at least one input sparse,
        e.g., ``block_diag([coo_matrix(A), B])``, or ``block_diag([coo_array(A), B])``.
        That removes any deprecation warnings as well.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        Handling of this no sparse input case will change no earlier than v1.20.

    Parameters
    ----------
    mats : sequence of matrices or arrays
        Input matrices or arrays.
    format : str, optional
        The sparse format of the result (e.g., "csr"). If not given, the result
        is returned in "coo" format.
    dtype : dtype specifier, optional
        The data-type of the output. If not given, the dtype is
        determined from that of `blocks`.

    Returns
    -------
    res : sparse matrix or array
        If at least one input is a sparse array, the output is a sparse array.
        Otherwise the output is a sparse matrix.

    See Also
    --------
    block_array
    diags_array

    Notes
    -----

    .. versionadded:: 0.11.0

    Examples
    --------
    >>> from scipy.sparse import coo_array, block_diag
    >>> A = coo_array([[1, 2], [3, 4]])
    >>> B = coo_array([[5], [6]])
    >>> C = coo_array([[7]])
    >>> block_diag((A, B, C)).toarray()
    array([[1, 2, 0, 0],
           [3, 4, 0, 0],
           [0, 0, 5, 0],
           [0, 0, 6, 0],
           [0, 0, 0, 7]])
    """
    if any(isinstance(a, sparray) for a in mats):
        container = coo_array
    elif any(isinstance(a, spmatrix) for a in mats):
        container = coo_matrix
    else:  # all dense
        msg = """`block_diag` is switching to the sparse array interface.

        For the case where input arrays are numpy arrays, this function is
        switching to returning a sparse array instead of sparse matrix.
        Recover the sparse matrix return value by making one input a sparse matrix.
        For example, block_diag([coo_matrix(A), B]).
        Avoid this message for sparse array output using block_diag([coo_array(A), B]).
        For more information, see the spmatrix to sparray migration guide
        https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html

        This function will be changed no earlier than v1.20.
        """
        prefixes = (os.path.dirname(__file__),)
        warn(msg, category=DeprecationWarning, skip_file_prefixes=prefixes)

        # default when all input are ndarray
        container = coo_matrix

    row = []
    col = []
    data = []
    idx_arrays = []  # track idx_dtype of incoming sparse arrays
    r_idx = 0
    c_idx = 0
    for a in mats:
        if isinstance(a, (list | numbers.Number)):
            a = coo_array(np.atleast_2d(a))
        if issparse(a):
            a = a.tocoo()
            if not idx_arrays and a.coords[0].dtype == np.int64:
                idx_arrays.append(a.coords[0])
            nrows, ncols = a._shape_as_2d
            row.append(a.row + r_idx)
            col.append(a.col + c_idx)
            data.append(a.data)
        else:
            nrows, ncols = a.shape
            a_row, a_col = np.divmod(np.arange(nrows*ncols), ncols)
            row.append(a_row + r_idx)
            col.append(a_col + c_idx)
            data.append(a.ravel())
        r_idx += nrows
        c_idx += ncols
    idx_dtype = get_index_dtype(idx_arrays, maxval=max(r_idx, c_idx))
    row = np.concatenate(row, dtype=idx_dtype)
    col = np.concatenate(col, dtype=idx_dtype)
    data = np.concatenate(data)
    new_shape = (r_idx, c_idx)

    return container((data, (row, col)), shape=new_shape, dtype=dtype).asformat(format)


def block_diag(*arrs: ArrayLike) -> Array:
  """Create a block diagonal matrix from input arrays.

  JAX implementation of :func:`scipy.linalg.block_diag`.

  Args:
    *arrs: arrays of at most two dimensions

  Returns:
    2D block-diagonal array constructed by placing the input arrays
    along the diagonal.

  Examples:
    >>> A = jnp.ones((1, 1))
    >>> B = jnp.ones((2, 2))
    >>> C = jnp.ones((3, 3))
    >>> jax.scipy.linalg.block_diag(A, B, C)
    Array([[1., 0., 0., 0., 0., 0.],
           [0., 1., 1., 0., 0., 0.],
           [0., 1., 1., 0., 0., 0.],
           [0., 0., 0., 1., 1., 1.],
           [0., 0., 0., 1., 1., 1.],
           [0., 0., 0., 1., 1., 1.]], dtype=float32)
  """
  if len(arrs) == 0:
    arrs = (jnp.zeros((1, 0)),)
  arrs = tuple(promote_dtypes(*arrs))
  bad_shapes = [i for i, a in enumerate(arrs) if np.ndim(a) > 2]
  if bad_shapes:
    raise ValueError("Arguments to jax.scipy.linalg.block_diag must have at "
                     "most 2 dimensions, got {} at argument {}."
                     .format(arrs[bad_shapes[0]], bad_shapes[0]))
  converted_arrs = [jnp.atleast_2d(a) for a in arrs]
  dtype = lax.dtype(converted_arrs[0])
  total_cols = sum(a.shape[1] for a in converted_arrs)

  padded_arrs = []
  current_col = 0
  for arr in converted_arrs:
    cols = arr.shape[1]
    padding_config = ((0, 0, 0), (current_col, total_cols - cols - current_col, 0))
    padded_arrs.append(lax.pad(arr, dtype.type(0), padding_config))
    current_col += cols
  return jnp.concatenate(padded_arrs, axis=0)

