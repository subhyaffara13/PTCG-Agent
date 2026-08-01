
def spatial_offset_downsample(image_features: torch.Tensor, orig_side: int, offset: int = 0) -> torch.Tensor:
    """Sample one position from each 2x2 block; offset selects which corner (0=TL,1=TR,2=BL,3=BR)."""
    offset_h, offset_w = [(0, 0), (0, 1), (1, 0), (1, 1)][offset]
    new_side = orig_side // 2
    batch, _, channels = image_features.shape
    grid = image_features.reshape(batch, orig_side, orig_side, channels)
    grid = grid.reshape(batch, new_side, 2, new_side, 2, channels)
    return grid[:, :, offset_h, :, offset_w, :].reshape(batch, -1, channels)


def spatial_offset_downsample(image_features: torch.Tensor, orig_side: int, offset: int = 0) -> torch.Tensor:
    """Sample one position from each 2x2 block; offset selects which corner (0=TL,1=TR,2=BL,3=BR)."""
    offset_h, offset_w = [(0, 0), (0, 1), (1, 0), (1, 1)][offset]
    new_side = orig_side // 2
    batch, _, channels = image_features.shape
    grid = image_features.reshape(batch, orig_side, orig_side, channels)
    grid = grid.reshape(batch, new_side, 2, new_side, 2, channels)
    return grid[:, :, offset_h, :, offset_w, :].reshape(batch, -1, channels)

