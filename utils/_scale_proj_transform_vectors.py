
def _scale_proj_transform_vectors(vecs, axes):
    """
    Apply scale transforms and project vectors.

    Parameters
    ----------
    vecs : ... x 3 np.ndarray
        Input vectors.
    axes : Axes3D
        The 3D axes (used for scale transforms and projection matrix).
    """
    result_shape = vecs.shape
    xs, ys, zs = _apply_scale_transforms(
        vecs[..., 0], vecs[..., 1], vecs[..., 2], axes)
    vec = _vec_pad_ones(xs.ravel(), ys.ravel(), zs.ravel())
    product = np.dot(axes.M, vec)
    tvecs = product[:3] / product[3]
    return tvecs.T.reshape(result_shape)

