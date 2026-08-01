
def fuse_feature_maps(feature_map_1: torch.Tensor, feature_map_2: torch.Tensor, fuse_op: str = "sum") -> torch.Tensor:
    """Fuses two feature maps via element-wise sum or channel-wise concatenation."""
    if fuse_op == "sum":
        return feature_map_1 + feature_map_2
    return torch.cat([feature_map_1, feature_map_2], dim=1)


def fuse_feature_maps(feature_map_1: torch.Tensor, feature_map_2: torch.Tensor, fuse_op: str = "sum") -> torch.Tensor:
    """Fuses two feature maps via element-wise sum or channel-wise concatenation."""
    if fuse_op == "sum":
        return feature_map_1 + feature_map_2
    return torch.cat([feature_map_1, feature_map_2], dim=1)

