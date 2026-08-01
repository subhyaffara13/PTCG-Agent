
def convert_to_rgb(image: ImageInput) -> ImageInput:
    """
    Converts an image to RGB format. Only converts if the image is of type PIL.Image.Image, otherwise returns the image
    as is.
    Args:
        image (Image):
            The image to convert.
    """
    requires_backends(convert_to_rgb, ["vision"])

    if not isinstance(image, PIL.Image.Image):
        return image

    if image.mode == "RGB":
        return image

    image = image.convert("RGB")
    return image


def convert_to_rgb(
    video: np.ndarray,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Convert video to RGB by blending the transparency layer if it's in RGBA format, otherwise simply returns it.

    Args:
        video (`np.ndarray`):
            The video to convert.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input video. If unset, will use the inferred format from the input.
    """
    if not isinstance(video, np.ndarray):
        raise TypeError(f"Video has to be a numpy array to convert to RGB format, but found {type(video)}")

    # np.array usually comes with ChannelDimension.LAST so let's convert it
    if input_data_format is None:
        input_data_format = infer_channel_dimension_format(video)
    video = to_channel_dimension_format(video, ChannelDimension.FIRST, input_channel_dim=input_data_format)

    # 3 channels for RGB already
    if video.shape[-3] == 3:
        return video

    # Grayscale video so we repeat it 3 times for each channel
    if video.shape[-3] == 1:
        return video.repeat(3, -3)

    if not (video[..., 3, :, :] < 255).any():
        return video

    # There is a transparency layer, blend it with a white background.
    # Calculate the alpha proportion for blending.
    alpha = video[..., 3, :, :] / 255.0
    video = (1 - alpha[..., None, :, :]) * 255 + alpha[..., None, :, :] * video[..., 3, :, :]
    return video


def convert_to_rgb(image: ImageInput) -> ImageInput:
    """
    Converts an image to RGB format. Only converts if the image is of type PIL.Image.Image, otherwise returns the image
    as is.
    """
    if not is_vision_available() or not isinstance(image, Image.Image):
        return image

    if image.mode == "RGB":
        return image

    image_rgba = image.convert("RGBA")
    background = Image.new("RGBA", image_rgba.size, (255, 255, 255))
    alpha_composite = Image.alpha_composite(background, image_rgba)
    alpha_composite = alpha_composite.convert("RGB")
    return alpha_composite


def convert_to_rgb(image: ImageInput) -> ImageInput:
    """
    Converts an image to RGB format. Only converts if the image is of type PIL.Image.Image, otherwise returns the image
    as is.
    """
    if not is_vision_available() or not isinstance(image, Image.Image):
        return image

    if image.mode == "RGB":
        return image

    image_rgba = image.convert("RGBA")
    background = Image.new("RGBA", image_rgba.size, (255, 255, 255))
    alpha_composite = Image.alpha_composite(background, image_rgba)
    alpha_composite = alpha_composite.convert("RGB")
    return alpha_composite


def convert_to_rgb(image: ImageInput) -> ImageInput:
    """
    Converts an image to RGB format. Only converts if the image is of type PIL.Image.Image, otherwise returns the image
    as is.
    """
    if not is_vision_available() or not isinstance(image, Image.Image):
        return image

    if image.mode == "RGB":
        return image

    image_rgba = image.convert("RGBA")
    background = Image.new("RGBA", image_rgba.size, (255, 255, 255))
    alpha_composite = Image.alpha_composite(background, image_rgba)
    alpha_composite = alpha_composite.convert("RGB")
    return alpha_composite


def convert_to_rgb(image: ImageInput) -> ImageInput:
    """
    Converts an image to RGB format. Only converts if the image is of type PIL.Image.Image, otherwise returns the image
    as is.
    """
    if not is_vision_available() or not isinstance(image, Image.Image):
        return image

    if image.mode == "RGB":
        return image

    image_rgba = image.convert("RGBA")
    background = Image.new("RGBA", image_rgba.size, (255, 255, 255))
    alpha_composite = Image.alpha_composite(background, image_rgba)
    alpha_composite = alpha_composite.convert("RGB")
    return alpha_composite

