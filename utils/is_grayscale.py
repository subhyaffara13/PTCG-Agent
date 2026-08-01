
def is_grayscale(
    image: "torch.Tensor",
):
    """Checks if an image is grayscale (all RGB channels are identical)."""
    if image.ndim < 3 or image.shape[0 if image.ndim == 3 else 1] == 1:
        return True
    return torch.all(image[..., 0, :, :] == image[..., 1, :, :]) and torch.all(
        image[..., 1, :, :] == image[..., 2, :, :]
    )


def is_grayscale(image: np.ndarray):
    if image.shape[0] == 1:
        return True
    return np.all(image[0, ...] == image[1, ...]) and np.all(image[1, ...] == image[2, ...])


def is_grayscale(
    image: "torch.Tensor",
):
    """Checks if an image is grayscale (all RGB channels are identical)."""
    if image.ndim < 3 or image.shape[0 if image.ndim == 3 else 1] == 1:
        return True
    return torch.all(image[..., 0, :, :] == image[..., 1, :, :]) and torch.all(
        image[..., 1, :, :] == image[..., 2, :, :]
    )


def is_grayscale(image: np.ndarray):
    if image.shape[0] == 1:
        return True
    return np.all(image[0, ...] == image[1, ...]) and np.all(image[1, ...] == image[2, ...])


def is_grayscale(image: np.ndarray):
    if image.shape[0] == 1:
        return True
    return np.all(image[0, ...] == image[1, ...]) and np.all(image[1, ...] == image[2, ...])


def is_grayscale(
    image: "torch.Tensor",
):
    """Checks if an image is grayscale (all RGB channels are identical)."""
    if image.ndim < 3 or image.shape[0 if image.ndim == 3 else 1] == 1:
        return True
    return torch.all(image[..., 0, :, :] == image[..., 1, :, :]) and torch.all(
        image[..., 1, :, :] == image[..., 2, :, :]
    )


def is_grayscale(image: np.ndarray) -> bool:
    """Checks if an image is grayscale (all RGB channels are identical)."""
    if image.shape[0] == 1:
        return True
    return np.all(image[0, ...] == image[1, ...]) and np.all(image[1, ...] == image[2, ...])


def is_grayscale(image: "torch.Tensor") -> bool:
    """Checks if an image is grayscale (all RGB channels are identical)."""
    if image.ndim < 3 or image.shape[0 if image.ndim == 3 else 1] == 1:
        return True
    return torch.all(image[..., 0, :, :] == image[..., 1, :, :]) and torch.all(
        image[..., 1, :, :] == image[..., 2, :, :]
    )

