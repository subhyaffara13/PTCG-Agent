
def has_backend_feature(
    device: torch.device | str | None, feature: BackendFeature
) -> bool:
    """See also V.graph.has_feature"""
    assert isinstance(feature, BackendFeature)
    return feature in get_backend_features(device)

