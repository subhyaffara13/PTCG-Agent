
def _rle_to_mask(rle: dict[str, Any]) -> np.ndarray:
    """Compute a binary mask from an uncompressed RLE."""
    height, width = rle["size"]
    mask = np.empty(height * width, dtype=bool)
    idx = 0
    parity = False
    for count in rle["counts"]:
        mask[idx : idx + count] = parity
        idx += count
        parity = not parity
    mask = mask.reshape(width, height)
    return mask.transpose()  # Reshape to original shape


def _rle_to_mask(rle: dict[str, Any]) -> torch.Tensor:
    """Compute a binary mask from an uncompressed RLE."""
    height, width = rle["size"]
    mask = torch.empty(height * width, dtype=bool)
    idx = 0
    parity = False
    for count in rle["counts"]:
        mask[idx : idx + count] = parity
        idx += count
        parity = not parity
    mask = mask.reshape(width, height)
    return mask.transpose(0, 1)  # Reshape to original shape


def _rle_to_mask(rle: dict[str, Any]) -> torch.Tensor:
    """Compute a binary mask from an uncompressed RLE."""
    height, width = rle["size"]
    mask = torch.empty(height * width, dtype=bool)
    idx = 0
    parity = False
    for count in rle["counts"]:
        mask[idx : idx + count] = parity
        idx += count
        parity = not parity
    mask = mask.reshape(width, height)
    return mask.transpose(0, 1)  # Reshape to original shape


def _rle_to_mask(rle: dict[str, Any]) -> torch.Tensor:
    """Compute a binary mask from an uncompressed RLE."""
    height, width = rle["size"]
    mask = torch.empty(height * width, dtype=bool)
    idx = 0
    parity = False
    for count in rle["counts"]:
        mask[idx : idx + count] = parity
        idx += count
        parity = not parity
    mask = mask.reshape(width, height)
    return mask.transpose(0, 1)  # Reshape to original shape

