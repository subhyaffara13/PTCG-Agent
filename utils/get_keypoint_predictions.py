
def get_keypoint_predictions(heatmaps: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Predict keypoint locations and confidence scores from heatmaps.

    Args:
        heatmaps: Shape `(num_persons, num_keypoints, height, width)`.

    Returns:
        locations: `(num_persons, num_keypoints, 2)` x/y in heatmap pixel coordinates.
        scores: `(num_persons, num_keypoints)` per-keypoint confidence.
    """
    num_persons, num_keypoints, _, heatmap_width = heatmaps.shape
    device = heatmaps.device
    heatmap_flat = heatmaps.reshape(num_persons, num_keypoints, -1)
    scores = heatmap_flat.amax(dim=-1)
    flat_index = heatmap_flat.argmax(dim=-1)
    locations_x = (flat_index % heatmap_width).float()
    locations_y = (flat_index // heatmap_width).float()
    locations = torch.where(
        scores.unsqueeze(-1) > 0.0,
        torch.stack([locations_x, locations_y], dim=-1),
        torch.full((num_persons, num_keypoints, 2), -1.0, device=device),
    )
    return locations, scores


def get_keypoint_predictions(heatmaps: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Predict keypoint locations and confidence scores from heatmaps.

    Args:
        heatmaps: Shape `(num_persons, num_keypoints, height, width)`.

    Returns:
        locations: `(num_persons, num_keypoints, 2)` x/y in heatmap pixel coordinates.
        scores: `(num_persons, num_keypoints)` per-keypoint confidence.
    """
    num_persons, num_keypoints, _, heatmap_width = heatmaps.shape
    device = heatmaps.device
    heatmap_flat = heatmaps.reshape(num_persons, num_keypoints, -1)
    scores = heatmap_flat.amax(dim=-1)
    flat_index = heatmap_flat.argmax(dim=-1)
    locations_x = (flat_index % heatmap_width).float()
    locations_y = (flat_index // heatmap_width).float()
    locations = torch.where(
        scores.unsqueeze(-1) > 0.0,
        torch.stack([locations_x, locations_y], dim=-1),
        torch.full((num_persons, num_keypoints, 2), -1.0, device=device),
    )
    return locations, scores


def get_keypoint_predictions(heatmaps: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Get keypoint predictions from score maps.

    Args:
        heatmaps (`np.ndarray` of shape `(batch_size, num_keypoints, height, width)`):
            Model predicted heatmaps.

    Returns:
        tuple: A tuple containing aggregated results.

        - coords (`np.ndarray` of shape `(batch_size, num_keypoints, 2)`):
            Predicted keypoint location.
        - scores (`np.ndarray` of shape `(batch_size, num_keypoints, 1)`):
            Scores (confidence) of the keypoints.
    """
    if not isinstance(heatmaps, np.ndarray):
        raise TypeError("Heatmaps should be np.ndarray")
    if heatmaps.ndim != 4:
        raise ValueError("Heatmaps should be 4-dimensional")

    batch_size, num_keypoints, _, width = heatmaps.shape
    heatmaps_reshaped = heatmaps.reshape((batch_size, num_keypoints, -1))
    idx = np.argmax(heatmaps_reshaped, 2).reshape((batch_size, num_keypoints, 1))
    scores = np.amax(heatmaps_reshaped, 2).reshape((batch_size, num_keypoints, 1))

    preds = np.tile(idx, (1, 1, 2)).astype(np.float32)
    preds[:, :, 0] = preds[:, :, 0] % width
    preds[:, :, 1] = preds[:, :, 1] // width

    preds = np.where(np.tile(scores, (1, 1, 2)) > 0.0, preds, -1)
    return preds, scores


def get_keypoint_predictions(heatmaps: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Get keypoint predictions from score maps.

    Args:
        heatmaps (`np.ndarray` of shape `(batch_size, num_keypoints, height, width)`):
            Model predicted heatmaps.

    Returns:
        tuple: A tuple containing aggregated results.

        - coords (`np.ndarray` of shape `(batch_size, num_keypoints, 2)`):
            Predicted keypoint location.
        - scores (`np.ndarray` of shape `(batch_size, num_keypoints, 1)`):
            Scores (confidence) of the keypoints.
    """
    if not isinstance(heatmaps, np.ndarray):
        raise TypeError("Heatmaps should be np.ndarray")
    if heatmaps.ndim != 4:
        raise ValueError("Heatmaps should be 4-dimensional")

    batch_size, num_keypoints, _, width = heatmaps.shape
    heatmaps_reshaped = heatmaps.reshape((batch_size, num_keypoints, -1))
    idx = np.argmax(heatmaps_reshaped, 2).reshape((batch_size, num_keypoints, 1))
    scores = np.amax(heatmaps_reshaped, 2).reshape((batch_size, num_keypoints, 1))

    preds = np.tile(idx, (1, 1, 2)).astype(np.float32)
    preds[:, :, 0] = preds[:, :, 0] % width
    preds[:, :, 1] = preds[:, :, 1] // width

    preds = np.where(np.tile(scores, (1, 1, 2)) > 0.0, preds, -1)
    return preds, scores

