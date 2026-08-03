from typing import Union

def get_max_height_width(
    images: list[Union["torch.Tensor", np.ndarray]], input_data_format: str | ChannelDimension = ChannelDimension.FIRST
) -> list[int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    if input_data_format == ChannelDimension.FIRST:
        _, max_height, max_width = max_across_indices([img.shape for img in images])
    elif input_data_format == ChannelDimension.LAST:
        max_height, max_width, _ = max_across_indices([img.shape for img in images])
    else:
        raise ValueError(f"Invalid channel dimension format: {input_data_format}")
    return (max_height, max_width)


def get_max_height_width(images_list: list[list["torch.Tensor|np.ndarray"]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(images_list: list[list["torch.Tensor|np.ndarray"]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(images_list: list[list["torch.Tensor|np.ndarray"]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(images_list: list[list[np.ndarray]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(images_list: list[list[np.ndarray]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(images_list: list[list["torch.Tensor|np.ndarray"]]) -> tuple[int, int]:
    """
    Get the maximum height and width across all images in a batch.
    """
    image_sizes = []
    for images in images_list:
        for image in images:
            image_sizes.append(image.shape[-2:])

    max_height = max(size[0] for size in image_sizes)
    max_width = max(size[1] for size in image_sizes)
    return (max_height, max_width)


def get_max_height_width(videos: list["torch.Tensor"]) -> list[int]:
    """
    Get the maximum height and width across all videos in a batch.
    """
    max_height = max_width = float("-inf")
    for video in videos:
        height, width = video.size()[-2:]
        max_height = max(height, max_height)
        max_width = max(width, max_width)
    return (max_height, max_width)

