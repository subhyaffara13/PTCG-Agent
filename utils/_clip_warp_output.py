
def _clip_warp_output(input_image, output_image):
    """Clip output image to range of values of input image.

    Note that this function modifies the values of *output_image* in-place.

    Taken from:
    https://github.com/scikit-image/scikit-image/blob/b4b521d6f0a105aabeaa31699949f78453ca3511/skimage/transform/_warps.py#L640.

    Args:
        input_image : ndarray
            Input image.
        output_image : ndarray
            Output image, which is modified in-place.
    """
    min_val = np.min(input_image)
    if np.isnan(min_val):
        # NaNs detected, use NaN-safe min/max
        min_func = np.nanmin
        max_func = np.nanmax
        min_val = min_func(input_image)
    else:
        min_func = np.min
        max_func = np.max
    max_val = max_func(input_image)

    output_image = np.clip(output_image, min_val, max_val)

    return output_image


def _clip_warp_output(input_image, output_image):
    """Clip output image to range of values of input image.

    Note that this function modifies the values of *output_image* in-place.

    Taken from:
    https://github.com/scikit-image/scikit-image/blob/b4b521d6f0a105aabeaa31699949f78453ca3511/skimage/transform/_warps.py#L640.

    Args:
        input_image : ndarray
            Input image.
        output_image : ndarray
            Output image, which is modified in-place.
    """
    min_val = np.min(input_image)
    if np.isnan(min_val):
        # NaNs detected, use NaN-safe min/max
        min_func = np.nanmin
        max_func = np.nanmax
        min_val = min_func(input_image)
    else:
        min_func = np.min
        max_func = np.max
    max_val = max_func(input_image)

    output_image = np.clip(output_image, min_val, max_val)

    return output_image

