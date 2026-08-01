
def _block(blocks, format, dtype, return_spmatrix=False):
    blocks = np.asarray(blocks, dtype='object')

    if blocks.ndim != 2:
        raise ValueError('blocks must be 2-D, and some must be sparse')

    M,N = blocks.shape

    # check for fast path cases
    if (format in (None, 'csr') and
        all(issparse(b) and b.format == 'csr' for b in blocks.flat)
    ):
        if N > 1:
            # stack along columns (axis 1): must have shape (M, 1)
            blocks = [[_stack_along_minor_axis(blocks[b, :], 1)] for b in range(M)]
            blocks = np.asarray(blocks, dtype='object')

        # stack along rows (axis 0):
        A = _compressed_sparse_stack(blocks[:, 0], 0, return_spmatrix)
        if dtype is not None:
            A = A.astype(dtype, copy=False)
        return A
    elif (format in (None, 'csc') and
          all(issparse(b) and b.format == 'csc' for b in blocks.flat)
    ):
        if M > 1:
            # stack along rows (axis 0): must have shape (1, N)
            blocks = [[_stack_along_minor_axis(blocks[:, b], 0) for b in range(N)]]
            blocks = np.asarray(blocks, dtype='object')

        # stack along columns (axis 1):
        A = _compressed_sparse_stack(blocks[0, :], 1, return_spmatrix)
        if dtype is not None:
            A = A.astype(dtype, copy=False)
        return A

    block_mask = np.zeros(blocks.shape, dtype=bool)
    brow_lengths = np.zeros(M, dtype=np.int64)
    bcol_lengths = np.zeros(N, dtype=np.int64)

    # convert everything to COO format
    for i in range(M):
        for j in range(N):
            if blocks[i,j] is not None:
                A = coo_array(blocks[i,j])
                blocks[i,j] = A
                block_mask[i,j] = True

                if brow_lengths[i] == 0:
                    brow_lengths[i] = A._shape_as_2d[0]
                elif brow_lengths[i] != A._shape_as_2d[0]:
                    msg = (f'blocks[{i},:] has incompatible row dimensions. '
                           f'Got blocks[{i},{j}].shape[0] == {A._shape_as_2d[0]}, '
                           f'expected {brow_lengths[i]}.')
                    raise ValueError(msg)

                if bcol_lengths[j] == 0:
                    bcol_lengths[j] = A._shape_as_2d[1]
                elif bcol_lengths[j] != A._shape_as_2d[1]:
                    msg = (f'blocks[:,{j}] has incompatible column '
                           f'dimensions. '
                           f'Got blocks[{i},{j}].shape[1] == {A._shape_as_2d[1]}, '
                           f'expected {bcol_lengths[j]}.')
                    raise ValueError(msg)

    nnz = sum(block.nnz for block in blocks[block_mask])
    if dtype is None:
        all_dtypes = [blk.dtype for blk in blocks[block_mask]]
        dtype = upcast(*all_dtypes) if all_dtypes else None

    row_offsets = np.append(0, np.cumsum(brow_lengths))
    col_offsets = np.append(0, np.cumsum(bcol_lengths))

    shape = (row_offsets[-1], col_offsets[-1])

    data = np.empty(nnz, dtype=dtype)
    idx_dtype = get_index_dtype([b.coords[0] for b in blocks[block_mask]],
                                maxval=max(shape))
    row = np.empty(nnz, dtype=idx_dtype)
    col = np.empty(nnz, dtype=idx_dtype)

    nnz = 0
    ii, jj = np.nonzero(block_mask)
    for i, j in zip(ii, jj):
        B = blocks[i, j]
        idx = slice(nnz, nnz + B.nnz)
        data[idx] = B.data
        np.add(B.row, row_offsets[i], out=row[idx], dtype=idx_dtype)
        np.add(B.col, col_offsets[j], out=col[idx], dtype=idx_dtype)
        nnz += B.nnz

    if return_spmatrix:
        return coo_matrix((data, (row, col)), shape=shape).asformat(format)
    return coo_array((data, (row, col)), shape=shape).asformat(format)


def _block(arrays, max_depth, result_ndim, depth=0):
    """
    Internal implementation of block based on repeated concatenation.
    `arrays` is the argument passed to
    block. `max_depth` is the depth of nested lists within `arrays` and
    `result_ndim` is the greatest of the dimensions of the arrays in
    `arrays` and the depth of the lists in `arrays` (see block docstring
    for details).
    """
    if depth < max_depth:
        arrs = [_block(arr, max_depth, result_ndim, depth + 1)
                for arr in arrays]
        return _concatenate(arrs, axis=-(max_depth - depth))
    else:
        # We've 'bottomed out' - arrays is either a scalar or an array
        # type(arrays) is not list
        return _atleast_nd(arrays, result_ndim)


def _block(xs: ArrayLike | list[ArrayLike]) -> tuple[Array, int]:
  if isinstance(xs, tuple):
    raise ValueError("jax.numpy.block does not allow tuples, got {}"
                     .format(xs))
  elif isinstance(xs, list):
    if len(xs) == 0:
      raise ValueError("jax.numpy.block does not allow empty list arguments")
    xs_tup, depths = unzip2([_block(x) for x in xs])
    if any(d != depths[0] for d in depths[1:]):
      raise ValueError("Mismatched list depths in jax.numpy.block")
    rank = max(depths[0], max(np.ndim(x) for x in xs_tup))
    xs_tup = tuple(_atleast_nd(x, rank) for x in xs_tup)
    return concatenate(xs_tup, axis=-depths[0]), depths[0] + 1
  else:
    return asarray(xs), 1

