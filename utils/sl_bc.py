
def sl_bc(ya, yb, p):
    return np.hstack((ya[0], yb[0], ya[1] - p[0]))

