
def _stack_along_minor_axis(blocks, axis):
    """
    Stacking fast path for CSR/CSC matrices along the minor axis
    (i) hstack for CSR, (ii) vstack for CSC.
    """
    n_blocks = len(blocks)
    if n_blocks == 0:
        raise ValueError('Missing block matrices')

    if n_blocks == 1:
        return blocks[0]

    # check for incompatible dimensions
    other_axis = 1 if axis == 0 else 0
    other_axis_dims = {b._shape_as_2d[other_axis] for b in blocks}
    if len(other_axis_dims) > 1:
        raise ValueError(f'Mismatching dimensions along axis {other_axis}: '
                         f'{other_axis_dims}')
    constant_dim, = other_axis_dims

    # Do the stacking
    indptr_list = [b.indptr for b in blocks]
    data_cat = np.concatenate([b.data for b in blocks])

    # Need to check if any indices/indptr, would be too large post-
    # concatenation for np.int32:
    # - The max value of indices is the output array's stacking-axis length - 1
    # - The max value in indptr is the number of non-zero entries. This is
    #   exceedingly unlikely to require int64, but is checked out of an
    #   abundance of caution.
    sum_dim = sum(b._shape_as_2d[axis] for b in blocks)
    nnz = sum(len(b.indices) for b in blocks)
    idx_dtype = get_index_dtype(indptr_list, maxval=max(sum_dim - 1, nnz))
    stack_dim_cat = np.array([b._shape_as_2d[axis] for b in blocks], dtype=idx_dtype)
    if data_cat.size > 0:
        indptr_cat = np.concatenate(indptr_list, dtype=idx_dtype)
        indices_cat = np.concatenate([b.indices for b in blocks], dtype=idx_dtype)
        indptr = np.empty(constant_dim + 1, dtype=idx_dtype)
        indices = np.empty_like(indices_cat)
        data = np.empty_like(data_cat)
        csr_hstack(n_blocks, constant_dim, stack_dim_cat,
                   indptr_cat, indices_cat, data_cat,
                   indptr, indices, data)
    else:
        indptr = np.zeros(constant_dim + 1, dtype=idx_dtype)
        indices = np.empty(0, dtype=idx_dtype)
        data = np.empty(0, dtype=data_cat.dtype)

    if axis == 0:
        return blocks[0]._csc_container((data, indices, indptr),
                          shape=(sum_dim, constant_dim))
    else:
        return blocks[0]._csr_container((data, indices, indptr),
                          shape=(constant_dim, sum_dim))

