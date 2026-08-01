
def get_valid_indices(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute flat indices of valid (non-padding) positions after one stride-2 conv, or pop `"valid_indices"` from `kwargs` if precomputed.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"valid_indices"` it is popped and returned.

    Returns:
        `(total_valid,)` flat indices into the `(num_chunks * max_len_after_conv)` grid.
    """
    if kwargs is not None and (valid_indices := kwargs.pop("valid_indices", None)) is not None:
        return valid_indices
    after_conv1 = (chunk_lengths - 1) // 2 + 1
    max_len = after_conv1.max().item()
    mask = torch.arange(max_len, device=chunk_lengths.device) < after_conv1.unsqueeze(1)
    return mask.flatten().nonzero().squeeze(-1)


def get_valid_indices(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute flat indices of valid (non-padding) positions after one stride-2 conv, or pop `"valid_indices"` from `kwargs` if precomputed.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"valid_indices"` it is popped and returned.

    Returns:
        `(total_valid,)` flat indices into the `(num_chunks * max_len_after_conv)` grid.
    """
    if kwargs is not None and (valid_indices := kwargs.pop("valid_indices", None)) is not None:
        return valid_indices
    after_conv1 = (chunk_lengths - 1) // 2 + 1
    max_len = after_conv1.max().item()
    mask = torch.arange(max_len, device=chunk_lengths.device) < after_conv1.unsqueeze(1)
    return mask.flatten().nonzero().squeeze(-1)


def get_valid_indices(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute flat indices of valid (non-padding) positions after CNN extraction, or pop `"valid_indices"` from `kwargs` if precomputed.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"valid_indices"` it is popped and returned.

    Returns:
        `(total_valid,)` flat indices into the `(num_chunks * max_len_after_cnn)` grid.
    """
    if kwargs is not None and (valid_indices := kwargs.pop("valid_indices", None)) is not None:
        return valid_indices
    feature_lens_after_cnn = _get_feat_extract_output_lengths(chunk_lengths)
    max_len_after_cnn = feature_lens_after_cnn.max().item()
    mask = torch.arange(max_len_after_cnn, device=chunk_lengths.device) < feature_lens_after_cnn.unsqueeze(1)
    return mask.flatten().nonzero().squeeze(-1)


def get_valid_indices(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute flat indices of valid (non-padding) positions after CNN extraction, or pop `"valid_indices"` from `kwargs` if precomputed.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"valid_indices"` it is popped and returned.

    Returns:
        `(total_valid,)` flat indices into the `(num_chunks * max_len_after_cnn)` grid.
    """
    if kwargs is not None and (valid_indices := kwargs.pop("valid_indices", None)) is not None:
        return valid_indices
    feature_lens_after_cnn = _get_feat_extract_output_lengths(chunk_lengths)
    max_len_after_cnn = feature_lens_after_cnn.max().item()
    mask = torch.arange(max_len_after_cnn, device=chunk_lengths.device) < feature_lens_after_cnn.unsqueeze(1)
    return mask.flatten().nonzero().squeeze(-1)

