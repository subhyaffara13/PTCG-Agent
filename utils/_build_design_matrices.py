
def _build_design_matrices(x, y, z, tx, ty, kx, ky):

    w_x = np.ones_like(x)
    w_y = np.ones_like(y)

    Ax, offset_x, nc_x = _dierckx.data_matrix(x, tx, kx, w_x)
    Ay, offset_y, nc_y = _dierckx.data_matrix(y, ty, ky, w_y)
    Q = z.copy()

    return (PackedMatrix(Ax, offset_x, nc_x),
            PackedMatrix(Ay, offset_y, nc_y),
            Q)

