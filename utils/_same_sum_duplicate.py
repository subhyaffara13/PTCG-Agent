
def _same_sum_duplicate(data, *inds, **kwargs):
    """Duplicates entries to produce the same matrix"""
    indptr = kwargs.pop('indptr', None)
    if np.issubdtype(data.dtype, np.bool_) or \
       np.issubdtype(data.dtype, np.unsignedinteger):
        if indptr is None:
            return (data,) + inds
        else:
            return (data,) + inds + (indptr,)

    zeros_pos = (data == 0).nonzero()

    # duplicate data
    data = data.repeat(2, axis=0)
    data[::2] -= 1
    data[1::2] = 1

    # don't spoil all explicit zeros
    if zeros_pos[0].size > 0:
        pos = tuple(p[0] for p in zeros_pos)
        pos1 = (2*pos[0],) + pos[1:]
        pos2 = (2*pos[0]+1,) + pos[1:]
        data[pos1] = 0
        data[pos2] = 0

    inds = tuple(indices.repeat(2) for indices in inds)

    if indptr is None:
        return (data,) + inds
    else:
        return (data,) + inds + (indptr * 2,)

