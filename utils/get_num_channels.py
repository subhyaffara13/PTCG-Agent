
def get_num_channels(images_list: list[list["torch.Tensor|np.ndarray"]]) -> int:
    """
    Get the number of channels across all images in a batch. Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].shape[0]

    raise ValueError("No images found in the batch.")


def get_num_channels(images_list: list[list[np.ndarray]]) -> int:
    """
    Get the number of channels across all images in a batch. Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].shape[0]

    raise ValueError("No images found in the batch.")


def get_num_channels(images_list: list[list[np.ndarray]]) -> int:
    """
    Get the number of channels across all images in a batch. Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].shape[0]

    raise ValueError("No images found in the batch.")


def get_num_channels(images_list: list[list["torch.Tensor|np.ndarray"]]) -> int:
    """
    Get the number of channels across all images in a batch. Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].shape[0]

    raise ValueError("No images found in the batch.")

