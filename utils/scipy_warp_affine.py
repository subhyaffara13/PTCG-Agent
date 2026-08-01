
def scipy_warp_affine(src, M, size):
    """
    This function implements cv2.warpAffine function using affine_transform in scipy. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.affine_transform.html and https://docs.opencv.org/4.x/d4/d61/tutorial_warp_affine.html for more details.

    Note: the original implementation of cv2.warpAffine uses cv2.INTER_LINEAR.
    """
    channels = [src[..., i] for i in range(src.shape[-1])]

    # Convert to a 3x3 matrix used by SciPy
    M_scipy = np.vstack([M, [0, 0, 1]])
    # If you have a matrix for the 'push' transformation, use its inverse (numpy.linalg.inv) in this function.
    M_inv = inv(M_scipy)
    M_inv[0, 0], M_inv[0, 1], M_inv[1, 0], M_inv[1, 1], M_inv[0, 2], M_inv[1, 2] = (
        M_inv[1, 1],
        M_inv[1, 0],
        M_inv[0, 1],
        M_inv[0, 0],
        M_inv[1, 2],
        M_inv[0, 2],
    )

    new_src = [affine_transform(channel, M_inv, output_shape=size, order=1) for channel in channels]
    new_src = np.stack(new_src, axis=-1)
    return new_src


def scipy_warp_affine(src, M, size):
    """
    This function implements cv2.warpAffine function using affine_transform in scipy. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.affine_transform.html and https://docs.opencv.org/4.x/d4/d61/tutorial_warp_affine.html for more details.

    Note: the original implementation of cv2.warpAffine uses cv2.INTER_LINEAR.
    """
    channels = [src[..., i] for i in range(src.shape[-1])]

    # Convert to a 3x3 matrix used by SciPy
    M_scipy = np.vstack([M, [0, 0, 1]])
    # If you have a matrix for the 'push' transformation, use its inverse (numpy.linalg.inv) in this function.
    M_inv = inv(M_scipy)
    M_inv[0, 0], M_inv[0, 1], M_inv[1, 0], M_inv[1, 1], M_inv[0, 2], M_inv[1, 2] = (
        M_inv[1, 1],
        M_inv[1, 0],
        M_inv[0, 1],
        M_inv[0, 0],
        M_inv[1, 2],
        M_inv[0, 2],
    )

    new_src = [affine_transform(channel, M_inv, output_shape=size, order=1) for channel in channels]
    new_src = np.stack(new_src, axis=-1)
    return new_src

