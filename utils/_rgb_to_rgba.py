
def _rgb_to_rgba(A):
    """
    Convert an RGB image to RGBA, as required by the image resample C++
    extension.
    """
    rgba = np.zeros((A.shape[0], A.shape[1], 4), dtype=A.dtype)
    rgba[:, :, :3] = A
    if rgba.dtype == np.uint8:
        rgba[:, :, 3] = 255
    else:
        rgba[:, :, 3] = 1.0
    return rgba

