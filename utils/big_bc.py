
def big_bc(ya, yb):
    return np.hstack((ya[::2], yb[::2] - 1))

