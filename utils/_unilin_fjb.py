
def _unilin_fjb(B, x):
    _ret = np.concatenate((x, np.ones(x.shape, float)))
    return _ret.reshape((2,) + x.shape)

