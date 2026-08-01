
def get_matches_from_scores(scores: torch.Tensor, threshold: float) -> tuple[torch.Tensor, torch.Tensor]:
    """obtain matches from a score matrix [Bx M+1 x N+1]"""
    batch_size, _, _ = scores.shape
    # For each keypoint, get the best match
    max0 = scores[:, :-1, :-1].max(2)
    max1 = scores[:, :-1, :-1].max(1)
    matches0 = max0.indices
    matches1 = max1.indices

    # Mutual check for matches
    indices0 = torch.arange(matches0.shape[1], device=matches0.device)[None]
    indices1 = torch.arange(matches1.shape[1], device=matches1.device)[None]
    mutual0 = indices0 == matches1.gather(1, matches0)
    mutual1 = indices1 == matches0.gather(1, matches1)

    # Get matching scores and filter based on mutual check and thresholding
    max0 = max0.values.exp()
    zero = max0.new_tensor(0)
    matching_scores0 = torch.where(mutual0, max0, zero)
    matching_scores1 = torch.where(mutual1, matching_scores0.gather(1, matches1), zero)
    valid0 = mutual0 & (matching_scores0 > threshold)
    valid1 = mutual1 & valid0.gather(1, matches1)

    # Filter matches based on mutual check and thresholding of scores
    matches0 = torch.where(valid0, matches0, -1)
    matches1 = torch.where(valid1, matches1, -1)
    matches = torch.stack([matches0, matches1]).transpose(0, 1).reshape(batch_size * 2, -1)
    matching_scores = torch.stack([matching_scores0, matching_scores1]).transpose(0, 1).reshape(batch_size * 2, -1)

    return matches, matching_scores


def get_matches_from_scores(scores: torch.Tensor, threshold: float) -> tuple[torch.Tensor, torch.Tensor]:
    """obtain matches from a score matrix [Bx M+1 x N+1]"""
    batch_size, _, _ = scores.shape
    # For each keypoint, get the best match
    max0 = scores[:, :-1, :-1].max(2)
    max1 = scores[:, :-1, :-1].max(1)
    matches0 = max0.indices
    matches1 = max1.indices

    # Mutual check for matches
    indices0 = torch.arange(matches0.shape[1], device=matches0.device)[None]
    indices1 = torch.arange(matches1.shape[1], device=matches1.device)[None]
    mutual0 = indices0 == matches1.gather(1, matches0)
    mutual1 = indices1 == matches0.gather(1, matches1)

    # Get matching scores and filter based on mutual check and thresholding
    max0 = max0.values.exp()
    zero = max0.new_tensor(0)
    matching_scores0 = torch.where(mutual0, max0, zero)
    matching_scores1 = torch.where(mutual1, matching_scores0.gather(1, matches1), zero)
    valid0 = mutual0 & (matching_scores0 > threshold)
    valid1 = mutual1 & valid0.gather(1, matches1)

    # Filter matches based on mutual check and thresholding of scores
    matches0 = torch.where(valid0, matches0, -1)
    matches1 = torch.where(valid1, matches1, -1)
    matches = torch.stack([matches0, matches1]).transpose(0, 1).reshape(batch_size * 2, -1)
    matching_scores = torch.stack([matching_scores0, matching_scores1]).transpose(0, 1).reshape(batch_size * 2, -1)

    return matches, matching_scores

