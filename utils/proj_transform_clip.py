
def proj_transform_clip(xs, ys, zs, M):
    vec = _vec_pad_ones(xs, ys, zs)
    return _proj_transform_vec_clip(vec, M, focal_length=np.inf)

