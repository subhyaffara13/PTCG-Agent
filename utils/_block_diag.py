
def _block_diag(self):
    """
    Converts an N-D COO array into a 2-D COO array in block diagonal form.

    Parameters:
    self (coo_array): An N-Dimensional COO sparse array.

    Returns:
    coo_array: A 2-Dimensional COO sparse array in block diagonal form.
    """
    if self.ndim<2:
        raise ValueError("array must have atleast dim=2")
    num_blocks = math.prod(self.shape[:-2])
    n_col = self.shape[-1]
    n_row = self.shape[-2]
    res_arr = self.reshape((num_blocks, n_row, n_col))
    new_coords = (
        res_arr.coords[1] + res_arr.coords[0] * res_arr.shape[1],
        res_arr.coords[2] + res_arr.coords[0] * res_arr.shape[2],
    )

    new_shape = (num_blocks * n_row, num_blocks * n_col)
    return coo_array((self.data, tuple(new_coords)), shape=new_shape)

