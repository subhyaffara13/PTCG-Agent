
def _get_sparse_data_and_coords(x, new_shape, dtype):
    x = x.tocoo()
    x.sum_duplicates()

    x_coords = list(x.coords)
    x_data = x.data.astype(dtype, copy=False)
    x_shape = x.shape

    if new_shape == x_shape:
        return x_data, x_coords

    # broadcasting needed
    len_diff = len(new_shape) - len(x_shape)
    if len_diff > 0:
        # prepend ones to shape of x to match ndim
        x_shape = [1] * len_diff + list(x_shape)
        coord_zeros = np.zeroslike(x_coords[0])
        x_coords = tuple([coord_zeros] * len_diff + x_coords)
    # taking away axes (squeezing) is not part of broadcasting, but long
    # spmatrix history of using 2d vectors in 1d space, so we manually
    # squeeze the front and back axes here to be compatible
    if len_diff < 0:
        for _ in range(-len_diff):
            if x_shape[0] == 1:
                x_shape = x_shape[1:]
                x_coords = x_coords[1:]
            elif x_shape[-1] == 1:
                x_shape = x_shape[:-1]
                x_coords = x_coords[:-1]
            else:
                raise ValueError("shape mismatch in assignment")
    # broadcast with copy (will need to copy eventually anyway)
    tot_expand = 1
    for i, (nn, nx) in enumerate(zip(new_shape, x_shape)):
        if nn == nx:
            continue
        if nx != 1:
            raise ValueError("shape mismatch in assignment")
        x_nnz = len(x_coords[0])
        x_coords[i] = np.repeat(np.arange(nn), x_nnz)
        for j, co in enumerate(x_coords):
            if j == i:
                continue
            x_coords[j] = np.tile(co, nn)
        tot_expand *= nn
    x_data = np.tile(x_data.ravel(), tot_expand)
    return x_data, x_coords

