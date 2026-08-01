
def _compressed_sparse_stack(blocks, axis, return_spmatrix):
    """
    Stacking fast path for CSR/CSC matrices or arrays
    (i) vstack for CSR, (ii) hstack for CSC.
    """
    other_axis = 1 if axis == 0 else 0
    data = np.concatenate([b.data for b in blocks])
    constant_dim = blocks[0]._shape_as_2d[other_axis]
    idx_dtype = get_index_dtype(arrays=[b.indptr for b in blocks],
                                maxval=max(data.size, constant_dim))
    indices = np.empty(data.size, dtype=idx_dtype)
    indptr = np.empty(sum(b._shape_as_2d[axis] for b in blocks) + 1, dtype=idx_dtype)
    last_indptr = idx_dtype(0)
    sum_dim = 0
    sum_indices = 0
    for b in blocks:
        if b._shape_as_2d[other_axis] != constant_dim:
            raise ValueError(f'incompatible dimensions for axis {other_axis}')
        indices[sum_indices:sum_indices+b.indices.size] = b.indices
        sum_indices += b.indices.size
        idxs = slice(sum_dim, sum_dim + b._shape_as_2d[axis])
        indptr[idxs] = b.indptr[:-1]
        indptr[idxs] += last_indptr
        sum_dim += b._shape_as_2d[axis]
        last_indptr += b.indptr[-1]
    indptr[-1] = last_indptr
    # TODO remove this if-structure when sparse matrices removed
    if return_spmatrix:
        if axis == 0:
            return csr_matrix((data, indices, indptr),
                              shape=(sum_dim, constant_dim))
        else:
            return csc_matrix((data, indices, indptr),
                              shape=(constant_dim, sum_dim))

    if axis == 0:
        return csr_array((data, indices, indptr),
                          shape=(sum_dim, constant_dim))
    else:
        return csc_array((data, indices, indptr),
                          shape=(constant_dim, sum_dim))

