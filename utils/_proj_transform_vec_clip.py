
def _proj_transform_vec_clip(vec, M, focal_length):
    vecw = np.dot(M, vec.data)
    txs, tys, tzs = vecw[0:3] / vecw[3]
    if np.isinf(focal_length):  # don't clip orthographic projection
        tis = np.ones(txs.shape, dtype=bool)
    else:
        tis = (-1 <= txs) & (txs <= 1) & (-1 <= tys) & (tys <= 1) & (tzs <= 0)
    if np.ma.isMA(vec[0]):
        tis = tis & ~vec[0].mask
    if np.ma.isMA(vec[1]):
        tis = tis & ~vec[1].mask
    if np.ma.isMA(vec[2]):
        tis = tis & ~vec[2].mask

    txs = np.ma.masked_array(txs, ~tis)
    tys = np.ma.masked_array(tys, ~tis)
    tzs = np.ma.masked_array(tzs, ~tis)
    return txs, tys, tzs, tis

