
def convert_to_grayscale(
    image: "torch.Tensor",
) -> "torch.Tensor":
    """
    Converts an image to grayscale format using the NTSC formula. Only support torch.Tensor.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (torch.Tensor):
            The image to convert.
    """
    if is_grayscale(image):
        return image
    return tvF.rgb_to_grayscale(image, num_output_channels=3)


def convert_to_grayscale(image: ImageInput) -> ImageInput:
    """
    Converts an image to grayscale format using the NTSC formula. Only support numpy and PIL Image.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (Image):
            The image to convert.
    """

    if isinstance(image, np.ndarray):
        if is_grayscale(image):
            return image

        gray_image = image[0, ...] * 0.2989 + image[1, ...] * 0.5870 + image[2, ...] * 0.1140
        gray_image = np.stack([gray_image] * 3, axis=0)
        return gray_image

    if not isinstance(image, Image.Image):
        return image

    image = image.convert("L")
    return image


def convert_to_grayscale(
    image: "torch.Tensor",
) -> "torch.Tensor":
    """
    Converts an image to grayscale format using the NTSC formula. Only support torch.Tensor.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (torch.Tensor):
            The image to convert.
    """
    if is_grayscale(image):
        return image
    return tvF.rgb_to_grayscale(image, num_output_channels=3)


def convert_to_grayscale(image: ImageInput) -> ImageInput:
    """
    Converts an image to grayscale format using the NTSC formula. Only support numpy and PIL Image.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (Image):
            The image to convert.
    """

    if isinstance(image, np.ndarray):
        if is_grayscale(image):
            return image

        gray_image = image[0, ...] * 0.2989 + image[1, ...] * 0.5870 + image[2, ...] * 0.1140
        gray_image = np.stack([gray_image] * 3, axis=0)
        return gray_image

    if not isinstance(image, Image.Image):
        return image

    image = image.convert("L")
    return image


def convert_to_grayscale(image: ImageInput) -> ImageInput:
    """
    Converts an image to grayscale format using the NTSC formula. Only support numpy and PIL Image.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (Image):
            The image to convert.
    """

    if isinstance(image, np.ndarray):
        if is_grayscale(image):
            return image

        gray_image = image[0, ...] * 0.2989 + image[1, ...] * 0.5870 + image[2, ...] * 0.1140
        gray_image = np.stack([gray_image] * 3, axis=0)
        return gray_image

    if not isinstance(image, Image.Image):
        return image

    image = image.convert("L")
    return image


def convert_to_grayscale(
    image: "torch.Tensor",
) -> "torch.Tensor":
    """
    Converts an image to grayscale format using the NTSC formula. Only support torch.Tensor.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (torch.Tensor):
            The image to convert.
    """
    if is_grayscale(image):
        return image
    return tvF.rgb_to_grayscale(image, num_output_channels=3)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Converts an image to grayscale format using the NTSC formula. Only support numpy arrays.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (np.ndarray):
            The image to convert.
    """
    if is_grayscale(image):
        return image

    gray_image = image[0, ...] * 0.2989 + image[1, ...] * 0.5870 + image[2, ...] * 0.1140
    gray_image = np.stack([gray_image] * 3, axis=0)
    return gray_image


def convert_to_grayscale(image: "torch.Tensor") -> "torch.Tensor":
    """
    Converts an image to grayscale format using the NTSC formula. Only support torch.Tensor.

    This function is supposed to return a 1-channel image, but it returns a 3-channel image with the same value in each
    channel, because of an issue that is discussed in :
    https://github.com/huggingface/transformers/pull/25786#issuecomment-1730176446

    Args:
        image (torch.Tensor):
            The image to convert.
    """
    if is_grayscale(image):
        return image
    return tvF.rgb_to_grayscale(image, num_output_channels=3)

