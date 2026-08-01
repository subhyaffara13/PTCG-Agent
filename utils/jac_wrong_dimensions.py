
def jac_wrong_dimensions(x, a=0.0):
    return np.atleast_3d(jac_trivial(x, a=a))

