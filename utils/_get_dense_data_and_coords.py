
def _get_dense_data_and_coords(x, new_shape):
    if x.shape != new_shape:
        x = np.broadcast_to(x.squeeze(), new_shape)
    # shift scalar input to 1d so has coords
    if new_shape == ():
        x_coords = tuple([np.array([0])] * len(new_shape))
        x_data = x.ravel()
    else:
        x_coords = x.nonzero()
        x_data = x[x_coords]
    return x_data, x_coords

