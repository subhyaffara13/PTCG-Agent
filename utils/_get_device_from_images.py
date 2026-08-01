
def _get_device_from_images(images, is_nested: bool) -> "torch.device":
    """
    Get the device from the first non-empty element in a (potentially nested) list of images.

    Handles cases like `images = [[], [image]]` where the first sublist may be empty.
    """
    if is_nested:
        for row in images:
            if isinstance(row, torch.Tensor):
                return row.device
            if isinstance(row, list) and len(row) > 0:
                return row[0].device
    return images[0].device

