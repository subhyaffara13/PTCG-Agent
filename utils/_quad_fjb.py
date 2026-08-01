
def _quad_fjb(B, x):
    _ret = np.concatenate((x*x, x, np.ones(x.shape, float)))
    return _ret.reshape((3,) + x.shape)

