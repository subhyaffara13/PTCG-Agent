
def exp_bc_jac(ya, yb):
    dbc_dya = np.array([
        [1, 0],
        [0, 0]
    ])
    dbc_dyb = np.array([
        [0, 0],
        [1, 0]
    ])
    return dbc_dya, dbc_dyb

