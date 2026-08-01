
def make_pixel_mask(image: "torch.Tensor", output_size: tuple[int, int]) -> "torch.Tensor":
    """
    Make a pixel mask for the image, where 1 indicates a valid pixel and 0 indicates padding.
    """
    input_height, input_width = image.shape[-2:]
    mask = torch.zeros(output_size, dtype=torch.int64, device=image.device)
    mask[:input_height, :input_width] = 1
    return mask


def make_pixel_mask(image: "torch.Tensor", output_size: tuple[int, int]) -> "torch.Tensor":
    """
    Make a pixel mask for the image, where 1 indicates a valid pixel and 0 indicates padding.

    Args:
        image (`torch.Tensor`):
            Image to make the pixel mask for.
        output_size (`Tuple[int, int]`):
            Output size of the mask.
    """
    input_height, input_width = image.shape[-2:]
    mask = torch.zeros(output_size, dtype=torch.int64, device=image.device)
    mask[:input_height, :input_width] = 1
    return mask


def make_pixel_mask(image: "torch.Tensor", output_size: tuple[int, int]) -> "torch.Tensor":
    """
    Make a pixel mask for the image, where 1 indicates a valid pixel and 0 indicates padding.

    Args:
        image (`torch.Tensor`):
            Image to make the pixel mask for.
        output_size (`Tuple[int, int]`):
            Output size of the mask.
    """

    input_height, input_width = image.shape[-2], image.shape[-1]
    mask = torch.zeros(output_size, dtype=torch.int64)
    mask[:input_height, :input_width] = 1
    return mask


def make_pixel_mask(image: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """
    Make a pixel mask for the image, where 1 indicates a valid pixel and 0 indicates padding.

    Args:
        image (`np.ndarray`):
            Image to make the pixel mask for.
        output_size (`Tuple[int, int]`):
            Output size of the mask.
    """
    input_height, input_width = get_image_size(image, channel_dim=ChannelDimension.FIRST)
    mask = np.zeros(output_size, dtype=np.int64)
    mask[:input_height, :input_width] = 1
    return mask


def make_pixel_mask(
    image: np.ndarray, output_size: tuple[int, int], input_data_format: str | ChannelDimension | None = None
) -> np.ndarray:
    """
    Make a pixel mask for the image, where 1 indicates a valid pixel and 0 indicates padding.

    Args:
        image (`np.ndarray`):
            Image to make the pixel mask for.
        output_size (`tuple[int, int]`):
            Output size of the mask.
    """
    input_height, input_width = get_image_size(image, channel_dim=input_data_format)
    mask = np.zeros(output_size, dtype=np.int64)
    mask[:input_height, :input_width] = 1
    return mask

