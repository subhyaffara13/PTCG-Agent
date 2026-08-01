
def big_bc_with_parameters(ya, yb, p):
    # big version of sl_bc, with two parameters
    return np.hstack((ya[::2], yb[::2], ya[1] - p[0], ya[3] - p[1]))

