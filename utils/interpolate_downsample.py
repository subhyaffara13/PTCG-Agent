
def interpolate_downsample(image_features: torch.Tensor, orig_side: int, new_side: int) -> torch.Tensor:
    """Spatial downsampling via area interpolation."""
    batch, _, channels = image_features.size()
    spatial = image_features.view(batch, orig_side, orig_side, channels).permute(0, 3, 1, 2)
    spatial = torch.nn.functional.interpolate(spatial, size=(new_side, new_side), mode="area")
    return spatial.permute(0, 2, 3, 1).flatten(1, 2)


def interpolate_downsample(image_features: torch.Tensor, orig_side: int, new_side: int) -> torch.Tensor:
    """Spatial downsampling via area interpolation."""
    batch, _, channels = image_features.size()
    spatial = image_features.view(batch, orig_side, orig_side, channels).permute(0, 3, 1, 2)
    spatial = torch.nn.functional.interpolate(spatial, size=(new_side, new_side), mode="area")
    return spatial.permute(0, 2, 3, 1).flatten(1, 2)

