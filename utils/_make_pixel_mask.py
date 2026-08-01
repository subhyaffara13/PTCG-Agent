
def _make_pixel_mask(image: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Make pixel mask: 1=valid, 0=padding. Images are CHW."""
    h, w = image.shape[-2:]
    mask = np.zeros(output_size, dtype=np.int64)
    mask[:h, :w] = 1
    return mask


def _make_pixel_mask(image: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Make pixel mask: 1=valid, 0=padding. Images are CHW."""
    h, w = image.shape[-2:]
    mask = np.zeros(output_size, dtype=np.int64)
    mask[:h, :w] = 1
    return mask


def _make_pixel_mask(image: np.ndarray, output_size: tuple[int, int]) -> np.ndarray:
    """Make pixel mask: 1=valid, 0=padding. Images are CHW."""
    h, w = image.shape[-2:]
    mask = np.zeros(output_size, dtype=np.int64)
    mask[:h, :w] = 1
    return mask

