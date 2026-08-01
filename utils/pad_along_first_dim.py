
def pad_along_first_dim(
    image: "torch.Tensor", positions: "torch.Tensor", target_length: int
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the tensor along the first dimension.
    """
    current_length = image.shape[0]
    padding_length = target_length - current_length
    if padding_length > 0:
        padding = [0, 0] * (image.ndim - 1) + [0, padding_length]
        pos_padding = (0, 0, 0, padding_length)
        image = torch.nn.functional.pad(image, padding, mode="constant", value=0)
        positions = torch.nn.functional.pad(positions, pos_padding, mode="constant", value=-1)
    return image, positions


def pad_along_first_dim(image: np.ndarray, positions: np.ndarray, target_length: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Pad the image along the first dimension.
    """
    current_length = image.shape[0]
    padding_length = target_length - current_length
    if padding_length > 0:
        paddings = [(0, padding_length)] + [(0, 0)] * (image.ndim - 1)
        pos_paddings = [(0, padding_length), (0, 0)]
        image = np.pad(image, paddings, mode="constant", constant_values=0)
        positions = np.pad(positions, pos_paddings, mode="constant", constant_values=-1)
    return image, positions


def pad_along_first_dim(
    image: "torch.Tensor", positions: "torch.Tensor", target_length: int
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the tensor along the first dimension.
    """
    current_length = image.shape[0]
    padding_length = target_length - current_length
    if padding_length > 0:
        padding = [0, 0] * (image.ndim - 1) + [0, padding_length]
        pos_padding = (0, 0, 0, padding_length)
        image = torch.nn.functional.pad(image, padding, mode="constant", value=0)
        positions = torch.nn.functional.pad(positions, pos_padding, mode="constant", value=-1)
    return image, positions


def pad_along_first_dim(
    images: "torch.Tensor", target_length: int, pad_value: int = 0
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the array along the first dimension.
    """
    current_length = images.shape[1]
    padding_length = target_length - current_length
    pixel_mask = torch.ones((target_length,), dtype=torch.int32)
    if padding_length > 0:
        paddings = (0, 0, 0, padding_length, 0, 0)
        images = torch.nn.functional.pad(images, paddings, mode="constant", value=pad_value)
        pixel_mask[-padding_length:] = 0
    return images, pixel_mask


def pad_along_first_dim(array: np.ndarray, target_length: int, pad_value: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """
    Pad the array along the first dimension.
    """
    current_length = array.shape[0]
    padding_length = target_length - current_length
    mask = np.ones((target_length,), dtype=np.int32)
    if padding_length > 0:
        paddings = [(0, padding_length)] + [(0, 0)] * (array.ndim - 1)
        array = np.pad(array, paddings, mode="constant", constant_values=pad_value)
        mask[-padding_length:] = 0
    return array, mask


def pad_along_first_dim(
    tensor: "torch.Tensor", target_length: int, pad_value: int = 0
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """
    Pad the tensor along the first dimension.
    """
    current_length = tensor.shape[0]
    padding_length = target_length - current_length
    mask = torch.ones((target_length,), dtype=torch.int32)
    if padding_length > 0:
        padding = [0, 0] * (tensor.ndim - 1) + [0, padding_length]
        tensor = torch.nn.functional.pad(tensor, padding, mode="constant", value=pad_value)
        mask[-padding_length:] = 0
    return tensor, mask

