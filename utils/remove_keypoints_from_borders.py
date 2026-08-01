
def remove_keypoints_from_borders(
    keypoints: torch.Tensor, scores: torch.Tensor, border: int, height: int, width: int
) -> tuple[torch.Tensor, torch.Tensor]:
    """Removes keypoints (and their associated scores) that are too close to the border"""
    mask_h = (keypoints[:, 0] >= border) & (keypoints[:, 0] < (height - border))
    mask_w = (keypoints[:, 1] >= border) & (keypoints[:, 1] < (width - border))
    mask = mask_h & mask_w
    return keypoints[mask], scores[mask]

