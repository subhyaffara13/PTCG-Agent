
def _extract_block_diag(self, shape):
    n_row, n_col = shape[-2], shape[-1]

    # Extract data and coordinates from the block diagonal COO array
    data = self.data
    row, col = self.row, self.col

    # Initialize new coordinates array
    new_coords = np.empty((len(shape), self.nnz), dtype=int)

    # Calculate within-block indices
    new_coords[-2] = row % n_row
    new_coords[-1] = col % n_col

    # Calculate coordinates for higher dimensions
    temp_block_idx = row // n_row
    for i in range(len(shape) - 3, -1, -1):
        size = shape[i]
        new_coords[i] = temp_block_idx % size
        temp_block_idx = temp_block_idx // size

    # Create the new COO array with the original n-D shape
    return coo_array((data, tuple(new_coords)), shape=shape)

