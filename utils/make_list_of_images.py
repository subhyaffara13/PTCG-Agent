
def make_list_of_images(images, expected_ndims: int = 3) -> list[ImageInput]:
    """
    Ensure that the output is a list of images. If the input is a single image, it is converted to a list of length 1.
    If the input is a batch of images, it is converted to a list of images.

    Args:
        images (`ImageInput`):
            Image or batch of images to turn into a list of images.
        expected_ndims (`int`, *optional*, defaults to 3):
            Expected number of dimensions for a single input image. If the input image has a different number of
            dimensions, an error is raised.
    """
    if is_batched(images):
        return images

    # Either the input is a single image, in which case we create a list of length 1
    if is_pil_image(images):
        # PIL images are never batched
        return [images]

    if is_valid_image(images):
        if images.ndim == expected_ndims + 1:
            # Batch of images
            images = list(images)
        elif images.ndim == expected_ndims:
            # Single image
            images = [images]
        else:
            raise ValueError(
                f"Invalid image shape. Expected either {expected_ndims + 1} or {expected_ndims} dimensions, but got"
                f" {images.ndim} dimensions."
            )
        return images
    raise ValueError(
        f"Invalid image type. Expected either PIL.Image.Image, numpy.ndarray, or torch.Tensor, but got {type(images)}."
    )

