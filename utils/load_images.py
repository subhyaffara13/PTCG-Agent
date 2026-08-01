
def load_images(
    images: Union[list, tuple, str, "PIL.Image.Image"], timeout: float | None = None
) -> Union["PIL.Image.Image", list["PIL.Image.Image"], list[list["PIL.Image.Image"]]]:
    """Loads images, handling different levels of nesting.

    Args:
      images: A single image, a list of images, or a list of lists of images to load.
      timeout: Timeout for loading images.

    Returns:
      A single image, a list of images, a list of lists of images.
    """
    if isinstance(images, (list, tuple)):
        if len(images) and isinstance(images[0], (list, tuple)):
            return [[load_image(image, timeout=timeout) for image in image_group] for image_group in images]
        else:
            return [load_image(image, timeout=timeout) for image in images]
    else:
        return load_image(images, timeout=timeout)

