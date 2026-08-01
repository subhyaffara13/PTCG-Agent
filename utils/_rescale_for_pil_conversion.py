
def _rescale_for_pil_conversion(image):
    """
    Detects whether or not the image needs to be rescaled before being converted to a PIL image.

    The assumption is that if the image is of type `np.float` and all values are between 0 and 1, it needs to be
    rescaled.
    """
    if image.dtype == np.uint8:
        do_rescale = False
    elif np.allclose(image, image.astype(int)):
        if np.all(image >= 0) and np.all(image <= 255):
            do_rescale = False
        else:
            raise ValueError(
                "The image to be converted to a PIL image contains values outside the range [0, 255], "
                f"got [{image.min()}, {image.max()}] which cannot be converted to uint8."
            )
    elif np.all(image >= 0) and np.all(image <= 1):
        do_rescale = True
    else:
        raise ValueError(
            "The image to be converted to a PIL image contains values outside the range [0, 1], "
            f"got [{image.min()}, {image.max()}] which cannot be converted to uint8."
        )
    return do_rescale

