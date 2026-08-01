
def _extract_submatrices(M, block_indices, block_size, axis):
    """
    Extract selected blocks of a matrices *M* depending on parameters
    *block_indices* and *block_size*.

    Returns the array of extracted matrices *Mres* so that ::

        M_res[..., ir, :] = M[(block_indices*block_size+ir), :]
    """
    assert block_indices.ndim == 1
    assert axis in [0, 1]

    r, c = M.shape
    if axis == 0:
        sh = [block_indices.shape[0], block_size, c]
    else:  # 1
        sh = [block_indices.shape[0], r, block_size]

    dt = M.dtype
    M_res = np.empty(sh, dtype=dt)
    if axis == 0:
        for ir in range(block_size):
            M_res[:, ir, :] = M[(block_indices*block_size+ir), :]
    else:  # 1
        for ic in range(block_size):
            M_res[:, :, ic] = M[:, (block_indices*block_size+ic)]

    return M_res

