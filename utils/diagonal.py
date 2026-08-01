
def diagonal(input, offset: int = 0, dim1: int = 0, dim2: int = 1):
    original_shape = input.get_size()
    num_dims = len(original_shape)
    dim1 = canonicalize_dim(idx=dim1, rank=num_dims)
    dim2 = canonicalize_dim(idx=dim2, rank=num_dims)

    check(
        dim1 != dim2, lambda: f"diagonal dimensions cannot be identical {dim1}, {dim2}"
    )

    offset_negative = V.graph.sizevars.evaluate_expr(sympy.Lt(offset, 0))
    if offset_negative:
        diag_size = V.graph.sizevars.evaluate_max(
            V.graph.sizevars.evaluate_min(
                original_shape[dim1] + offset,
                original_shape[dim2],
            ),
            0,  # type: ignore[arg-type]
        )
    else:
        diag_size = V.graph.sizevars.evaluate_max(
            V.graph.sizevars.evaluate_min(
                original_shape[dim1],
                original_shape[dim2] - offset,
            ),
            0,  # type: ignore[arg-type]
        )

    base_idx = (0, 0)
    if offset_negative:
        base_idx = (-offset, 0)
    else:
        base_idx = (0, offset)

    sizes = [s for i, s in enumerate(original_shape) if i not in (dim1, dim2)]
    sizes.append(diag_size)

    def reindexer(idx):
        diag_idx = idx[-1]
        original_idx = [0] * len(original_shape)
        cur_dim = 0
        for d in range(num_dims):
            if d == dim1:
                original_idx[d] = diag_idx + base_idx[0]
            elif d == dim2:
                original_idx[d] = diag_idx + base_idx[1]
            else:
                original_idx[d] = idx[cur_dim]
                cur_dim += 1

        assert cur_dim == len(original_shape) - 2
        return original_idx

    return TensorBox(ir.GenericView.create(input, sizes, reindexer))


def diagonal(a: ArrayLike, offset=0, axis1=0, axis2=1):
    axis1 = _util.normalize_axis_index(axis1, a.ndim)
    axis2 = _util.normalize_axis_index(axis2, a.ndim)
    return torch.diagonal(a, offset, axis1, axis2)


def diagonal(
    self: TensorLikeType,
    offset: int = 0,
    dim1: int = 0,
    dim2: int = 1,
) -> TensorLikeType:
    """
    Reference implementation of torch.diagonal
    """
    num_dims = self.dim()
    dim1 = utils.canonicalize_dim(idx=dim1, rank=num_dims)
    dim2 = utils.canonicalize_dim(idx=dim2, rank=num_dims)

    torch._check(
        dim1 != dim2, lambda: f"diagonal dimensions cannot be identical {dim1}, {dim2}"
    )

    storage_offset = self.storage_offset()

    # Use sym_min/sym_max to handle unbacked symbolic dimensions.
    if offset >= 0:
        diag_size = sym_max(sym_min(self.size()[dim1], self.size()[dim2] - offset), 0)
        storage_offset += offset * self.stride()[dim2]
    else:
        diag_size = sym_max(sym_min(self.size()[dim1] + offset, self.size()[dim2]), 0)
        storage_offset -= offset * self.stride()[dim1]

    sizes = [s for i, s in enumerate(self.size()) if i not in (dim1, dim2)]
    sizes.append(diag_size)

    strides = [s for i, s in enumerate(self.stride()) if i not in (dim1, dim2)]
    strides.append(self.stride()[dim1] + self.stride()[dim2])

    result = self.as_strided(size=sizes, stride=strides, storage_offset=storage_offset)

    return result


def diagonal(
    input: TensorLikeType,
    *,
    offset: int = 0,
    dim1: int = -2,
    dim2: int = -1,
) -> TensorLikeType:
    return torch.diagonal(input, offset=offset, dim1=dim1, dim2=dim2)


def diagonal(g: jit_utils.GraphContext, self, offset, dim1, dim2):
    rank = symbolic_helper._get_tensor_rank(self)
    # Replace negative indexing when rank is known
    if rank is not None:
        dim1 = dim1 if dim1 >= 0 else dim1 + rank
        dim2 = dim2 if dim2 >= 0 else dim2 + rank

    dim1_size = opset9.size(
        g, self, dim=g.op("Constant", value_t=torch.LongTensor([dim1]))
    )
    dim2_size = opset9.size(
        g, self, dim=g.op("Constant", value_t=torch.LongTensor([dim2]))
    )
    # Create appropriate mask
    mask_shape = g.op("Concat", dim1_size, dim2_size, axis_i=0)
    mask = opset9.zeros(g, mask_shape, None, None, None)
    mask = g.op("EyeLike", mask, k_i=offset)
    # dim1 and dim2 appended as a dimension at the end of the shape

    if rank is not None:
        axes = list(range(rank))
        axes.remove(dim1)
        axes.remove(dim2)
        self = g.op("Transpose", self, perm_i=axes + [dim1, dim2])
    else:
        return symbolic_helper._unimplemented("diagonal", "unknown input rank")

    # Multiply input and mask to calculate values along diagonal
    # The mask consists of one values where diagonal values are to be calculated
    # For example:
    # [[1.1, 1.2, 1.3],   *    [[1, 0, 0]   =   [[1.1, 0, 0],
    #  [2.1, 2.2, 2.3],         [0, 1, 0]        [0, 2.2, 0],
    #  [3.1, 3.2, 3.3]]         [0, 0, 1]]       [0, 0, 3.3]]
    result = g.op("Mul", self, mask)
    result = symbolic_helper._reducesum_helper(g, result, axes_i=[-1], keepdims_i=0)

    # Calculate gather indices based on offset and dims
    # If offset is greater than zero, set offset to zero as this aids in
    # calculation of selection window
    offset_op = g.op("Constant", value_t=torch.LongTensor([offset]))
    if offset >= 0:
        diag_size = g.op(
            "Max",
            g.op("Min", dim1_size, g.op("Sub", dim2_size, offset_op)),
            g.op("Constant", value_t=torch.LongTensor([0])),
        )
        offset = 0
    else:
        diag_size = g.op(
            "Max",
            g.op("Min", g.op("Add", dim1_size, offset_op), dim2_size),
            g.op("Constant", value_t=torch.LongTensor([0])),
        )
    diag_size = g.op("Concat", diag_size, axis_i=0)

    # Calculate which diagonal values to select
    # For example, in cases with offsets:
    # [[0, 1.1, 0]
    #  [0, 0, 2.2]]
    # we need to select the last two columns, so we create a tensor
    # with all columns that are to be selected
    # So in this example, it is [1, 2]
    select_window_ones_fill = opset9.ones(g, diag_size, 4, None, None)
    select_window = g.op(
        "CumSum",
        select_window_ones_fill,
        g.op("Constant", value_t=torch.LongTensor([0])),
    )
    select_window = g.op(
        "Add",
        select_window,
        g.op("Constant", value_t=torch.LongTensor([abs(offset) - 1])),
    )

    gather_shape = [
        opset9.size(g, result, dim=g.op("Constant", value_t=torch.LongTensor([axis])))
        for axis in list(range(rank))[:-2]
    ]
    gather_shape.append(diag_size)
    gather_shape = g.op("Concat", *gather_shape, axis_i=0)
    gather_indices = opset9.zeros(g, gather_shape, 4, None, None)

    # There might be cases where offset value is greater than number of rows/columns
    # and might cause the diagonal to overrun and as a result of this, diag_size would be zero.
    # For example, if
    #       offset = 9, dim1_size = 2 (columns), dim2_size = 4 (rows)
    #       diag_size = max(min(2, (4-9)), 0) = 0, based on calculation above
    # Cases with diagonal overrun always result in diag_size = max(0, -ve value) = 0
    # In cases without diagonal overrun, we select the appropriate rows/columns along which we
    # are calculating diagonal values. In cases with diagonal overrun, we return a tensor which has
    # the dimension of the row/column where overrun occurred as 0-dim, as we are essentially
    # returning an empty tensor
    overrun_cond = g.op(
        "Not",
        g.op(
            "Equal",
            diag_size,
            g.op("Constant", value_t=torch.tensor(0, dtype=torch.int64)),
        ),
    )

    if_op, (if_context, else_context), _ = jit_utils.add_op_with_blocks(
        g, "If", overrun_cond, n_blocks=2
    )

    gather_indices_if_block = if_context.op("Add", gather_indices, select_window)
    gather_indices_if_block = symbolic_helper._unsqueeze_helper(
        if_context, gather_indices_if_block, [rank - 1]
    )
    final_non_overrun = if_context.op(
        "GatherND", result, gather_indices_if_block, batch_dims_i=rank - 2
    )
    final_overrun = opset9.zeros(else_context, gather_shape, 6, None, None)
    utils._add_output_to_block(if_context.block, final_non_overrun)
    utils._add_output_to_block(else_context.block, final_overrun)
    return if_op


def diagonal(x: Array, /, xp: Namespace, *, offset: int = 0, **kwargs: object) -> Array:
    return xp.diagonal(x, offset=offset, axis1=-2, axis2=-1, **kwargs)


def diagonal(x, /, *, offset=0):
    """
    Returns specified diagonals of a matrix (or a stack of matrices) ``x``.

    This function is Array API compatible, contrary to
    :py:func:`numpy.diagonal`, the matrix is assumed
    to be defined by the last two dimensions.

    Parameters
    ----------
    x : (...,M,N) array_like
        Input array having shape (..., M, N) and whose innermost two
        dimensions form MxN matrices.
    offset : int, optional
        Offset specifying the off-diagonal relative to the main diagonal,
        where::

            * offset = 0: the main diagonal.
            * offset > 0: off-diagonal above the main diagonal.
            * offset < 0: off-diagonal below the main diagonal.

    Returns
    -------
    out : (...,min(N,M)) ndarray
        An array containing the diagonals and whose shape is determined by
        removing the last two dimensions and appending a dimension equal to
        the size of the resulting diagonals. The returned array must have
        the same data type as ``x``.

    See Also
    --------
    numpy.diagonal

    Examples
    --------
    >>> a = np.arange(4).reshape(2, 2); a
    array([[0, 1],
           [2, 3]])
    >>> np.linalg.diagonal(a)
    array([0, 3])

    A 3-D example:

    >>> a = np.arange(8).reshape(2, 2, 2); a
    array([[[0, 1],
            [2, 3]],
           [[4, 5],
            [6, 7]]])
    >>> np.linalg.diagonal(a)
    array([[0, 3],
           [4, 7]])

    Diagonals adjacent to the main diagonal can be obtained by using the
    `offset` argument:

    >>> a = np.arange(9).reshape(3, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> np.linalg.diagonal(a, offset=1)  # First superdiagonal
    array([1, 5])
    >>> np.linalg.diagonal(a, offset=2)  # Second superdiagonal
    array([2])
    >>> np.linalg.diagonal(a, offset=-1)  # First subdiagonal
    array([3, 7])
    >>> np.linalg.diagonal(a, offset=-2)  # Second subdiagonal
    array([6])

    The anti-diagonal can be obtained by reversing the order of elements
    using either `numpy.flipud` or `numpy.fliplr`.

    >>> a = np.arange(9).reshape(3, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> np.linalg.diagonal(np.fliplr(a))  # Horizontal flip
    array([2, 4, 6])
    >>> np.linalg.diagonal(np.flipud(a))  # Vertical flip
    array([6, 4, 2])

    Note that the order in which the diagonal is retrieved varies depending
    on the flip function.

    """
    return _core_diagonal(x, offset, axis1=-2, axis2=-1)


def diagonal(a, offset=0, axis1=0, axis2=1):
    """
    Return specified diagonals.

    If `a` is 2-D, returns the diagonal of `a` with the given offset,
    i.e., the collection of elements of the form ``a[i, i+offset]``.  If
    `a` has more than two dimensions, then the axes specified by `axis1`
    and `axis2` are used to determine the 2-D sub-array whose diagonal is
    returned.  The shape of the resulting array can be determined by
    removing `axis1` and `axis2` and appending an index to the right equal
    to the size of the resulting diagonals.

    In versions of NumPy prior to 1.7, this function always returned a new,
    independent array containing a copy of the values in the diagonal.

    In NumPy 1.7 and 1.8, it continues to return a copy of the diagonal,
    but depending on this fact is deprecated. Writing to the resulting
    array continues to work as it used to, but a FutureWarning is issued.

    Starting in NumPy 1.9 it returns a read-only view on the original array.
    Attempting to write to the resulting array will produce an error.

    In some future release, it will return a read/write view and writing to
    the returned array will alter your original array.  The returned array
    will have the same type as the input array.

    If you don't write to the array returned by this function, then you can
    just ignore all of the above.

    If you depend on the current behavior, then we suggest copying the
    returned array explicitly, i.e., use ``np.diagonal(a).copy()`` instead
    of just ``np.diagonal(a)``. This will work with both past and future
    versions of NumPy.

    Parameters
    ----------
    a : array_like
        Array from which the diagonals are taken.
    offset : int, optional
        Offset of the diagonal from the main diagonal.  Can be positive or
        negative.  Defaults to main diagonal (0).
    axis1 : int, optional
        Axis to be used as the first axis of the 2-D sub-arrays from which
        the diagonals should be taken.  Defaults to first axis (0).
    axis2 : int, optional
        Axis to be used as the second axis of the 2-D sub-arrays from
        which the diagonals should be taken. Defaults to second axis (1).

    Returns
    -------
    array_of_diagonals : ndarray
        If `a` is 2-D, then a 1-D array containing the diagonal and of the
        same type as `a` is returned unless `a` is a `matrix`, in which case
        a 1-D array rather than a (2-D) `matrix` is returned in order to
        maintain backward compatibility.

        If ``a.ndim > 2``, then the dimensions specified by `axis1` and `axis2`
        are removed, and a new axis inserted at the end corresponding to the
        diagonal.

    Raises
    ------
    ValueError
        If the dimension of `a` is less than 2.

    See Also
    --------
    diag : MATLAB work-a-like for 1-D and 2-D arrays.
    diagflat : Create diagonal arrays.
    trace : Sum along diagonals.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(4).reshape(2,2)
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> a.diagonal()
    array([0, 3])
    >>> a.diagonal(1)
    array([1])

    A 3-D example:

    >>> a = np.arange(8).reshape(2,2,2); a
    array([[[0, 1],
            [2, 3]],
           [[4, 5],
            [6, 7]]])
    >>> a.diagonal(0,  # Main diagonals of two arrays created by skipping
    ...            0,  # across the outer(left)-most axis last and
    ...            1)  # the "middle" (row) axis first.
    array([[0, 6],
           [1, 7]])

    The sub-arrays whose main diagonals we just obtained; note that each
    corresponds to fixing the right-most (column) axis, and that the
    diagonals are "packed" in rows.

    >>> a[:,:,0]  # main diagonal is [0 6]
    array([[0, 2],
           [4, 6]])
    >>> a[:,:,1]  # main diagonal is [1 7]
    array([[1, 3],
           [5, 7]])

    The anti-diagonal can be obtained by reversing the order of elements
    using either `numpy.flipud` or `numpy.fliplr`.

    >>> a = np.arange(9).reshape(3, 3)
    >>> a
    array([[0, 1, 2],
           [3, 4, 5],
           [6, 7, 8]])
    >>> np.fliplr(a).diagonal()  # Horizontal flip
    array([2, 4, 6])
    >>> np.flipud(a).diagonal()  # Vertical flip
    array([6, 4, 2])

    Note that the order in which the diagonal is retrieved varies depending
    on the flip function.
    """
    if isinstance(a, np.matrix):
        # Make diagonal of matrix 1-D to preserve backward compatibility.
        return asarray(a).diagonal(offset=offset, axis1=axis1, axis2=axis2)
    else:
        return asanyarray(a).diagonal(offset=offset, axis1=axis1, axis2=axis2)


def diagonal(a: ArrayLike, offset: int = 0, axis1: int = 0,
             axis2: int = 1) -> Array:
  """Returns the specified diagonal of an array.

  JAX implementation of :func:`numpy.diagonal`.

  The JAX version always returns a copy of the input, although if this is used
  within a JIT compilation, the compiler may avoid the copy.

  Args:
    a: Input array. Must be at least 2-dimensional.
    offset: optional, default=0. Diagonal offset from the main diagonal.
      Must be a static integer value. Can be positive or negative.
    axis1: optional, default=0. The first axis along which to take the diagonal.
    axis2: optional, default=1. The second axis along which to take the diagonal.

   Returns:
    A 1D array for 2D input, and in general a N-1 dimensional array
    for N-dimensional input.

  See also:
    - :func:`jax.numpy.diag`
    - :func:`jax.numpy.diagflat`

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.diagonal(x)
    Array([1, 5, 9], dtype=int32)
    >>> jnp.diagonal(x, offset=1)
    Array([2, 6], dtype=int32)
    >>> jnp.diagonal(x, offset=-1)
    Array([4, 8], dtype=int32)
  """
  a = util.ensure_arraylike("diagonal", a)

  if np.ndim(a) < 2:
    raise ValueError("diagonal requires an array of at least two dimensions.")
  offset = core.concrete_or_error(operator.index, offset, "'offset' argument of jnp.diagonal()")

  def _default_diag(a):
    a_shape = np.shape(a)

    a = moveaxis(a, (axis1, axis2), (-2, -1))

    diag_size = max(
        0, min(a_shape[axis1] + min(offset, 0), a_shape[axis2] - max(offset, 0))
    )
    i = arange(diag_size)
    j = arange(abs(offset), abs(offset) + diag_size)
    return a[..., i, j] if offset >= 0 else a[..., j, i]


  # The mosaic lowering rule for diag is only defined for square arrays.
  # TODO(mvoz): Add support for offsets.
  if np.shape(a)[0] != np.shape(a)[1] or np.ndim(a) != 2 or offset != 0 or a.dtype == bool:
    return _default_diag(a)
  else:
    a_shape_eye = eye(np.shape(a)[0], dtype=a.dtype)

    def _mosaic_diag(a):
      def _sum(x, axis):
        return lax.reduce(
            x,
            np.array(0, x.dtype),
            lax.add if x.dtype != bool else lax.bitwise_or,
            (axis,),
        )
      return _sum(lax.mul(a_shape_eye, a), axis=0)
    return control_flow.platform_dependent(a, default=_default_diag, mosaic=_mosaic_diag)


def diagonal(x: ArrayLike, /, *, offset: int = 0) -> Array:
  """Extract the diagonal of an matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.diagonal`.

  Args:
    x: array of shape ``(..., M, N)`` from which the diagonal will be extracted.
    offset: positive or negative offset from the main diagonal.

  Returns:
    Array of shape ``(..., K)`` where ``K`` is the length of the specified diagonal.

  See Also:
    - :func:`jax.numpy.diagonal`: more general functionality for extracting diagonals.
    - :func:`jax.numpy.diag`: create a diagonal matrix from values.

  Examples:
    Diagonals of a single matrix:

    >>> x = jnp.array([[1,  2,  3,  4],
    ...                [5,  6,  7,  8],
    ...                [9, 10, 11, 12]])
    >>> jnp.linalg.diagonal(x)
    Array([ 1,  6, 11], dtype=int32)
    >>> jnp.linalg.diagonal(x, offset=1)
    Array([ 2,  7, 12], dtype=int32)
    >>> jnp.linalg.diagonal(x, offset=-1)
    Array([ 5, 10], dtype=int32)

    Batched diagonals:

    >>> x = jnp.arange(24).reshape(2, 3, 4)
    >>> jnp.linalg.diagonal(x)
    Array([[ 0,  5, 10],
           [12, 17, 22]], dtype=int32)
  """
  x = ensure_arraylike('jnp.linalg.diagonal', x)
  return jnp.diagonal(x, offset=offset, axis1=-2, axis2=-1)

