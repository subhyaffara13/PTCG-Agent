
def get_device_from_images(images_list: list[list["torch.Tensor"]]) -> "torch.device":
    """
    Get the device from the first non-empty element in a nested list of images.
    Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].device


def get_device_from_images(images_list: list[list["torch.Tensor"]]) -> "torch.device":
    """
    Get the device from the first non-empty element in a nested list of images.
    Handle empty sublists like in [[], [image]].
    """
    for images in images_list:
        if images:
            return images[0].device

