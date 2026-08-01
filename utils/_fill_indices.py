
def _fill_indices(idx, dim, dim_size, elems_per_row, m, n, o):
    for i in range(1 if dim == 0 else m):
        for j in range(1 if dim == 1 else n):
            for k in range(1 if dim == 2 else o):
                ii = [i, j, k]
                ii[dim] = slice(0, idx.size(dim) + 1)
                idx[tuple(ii)] = torch.randperm(dim_size)[0:elems_per_row]

