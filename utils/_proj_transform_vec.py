
def _proj_transform_vec(vec, M):
    vecw = np.dot(M, vec.data)
    ts = vecw[0:3]/vecw[3]
    if np.ma.isMA(vec):
        ts = np.ma.array(ts, mask=vec.mask)
    return ts[0], ts[1], ts[2]

