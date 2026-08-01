
def get_audio_cu_seqlens(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute cumulative sequence lengths for audio attention, or pop `"cu_seqlens"` from `kwargs` if precomputed.

    Applies one stride-2 convolution length reduction, then returns cumulative
    boundaries for flash-attention-style sequence packing.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"cu_seqlens"` it is popped and returned.

    Returns:
        `(num_chunks + 1,)` int32 cumulative sequence boundaries.
    """
    if kwargs is not None and (cu_seqlens := kwargs.pop("cu_seqlens", None)) is not None:
        return cu_seqlens
    after_conv1 = (chunk_lengths - 1) // 2 + 1
    return F.pad(after_conv1.cumsum(0), (1, 0), value=0).to(torch.int32)


def get_audio_cu_seqlens(chunk_lengths: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute cumulative sequence lengths for audio attention, or pop `"cu_seqlens"` from `kwargs` if precomputed.

    Applies one stride-2 convolution length reduction, then returns cumulative
    boundaries for flash-attention-style sequence packing.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        kwargs: optional caller kwargs — if it contains `"cu_seqlens"` it is popped and returned.

    Returns:
        `(num_chunks + 1,)` int32 cumulative sequence boundaries.
    """
    if kwargs is not None and (cu_seqlens := kwargs.pop("cu_seqlens", None)) is not None:
        return cu_seqlens
    after_conv1 = (chunk_lengths - 1) // 2 + 1
    return F.pad(after_conv1.cumsum(0), (1, 0), value=0).to(torch.int32)


def get_audio_cu_seqlens(
    chunk_lengths: torch.Tensor,
    feature_lens: torch.Tensor,
    n_window_infer: int,
    n_window: int,
    kwargs: dict | None = None,
) -> torch.Tensor:
    """Compute cumulative sequence lengths for audio attention windowing, or pop `"cu_seqlens"` from `kwargs` if precomputed.

    Splits each sample's post-CNN features into inference windows and returns
    cumulative boundaries for flash-attention-style sequence packing.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window_infer: inference window size (in raw frames).
        n_window: half the chunk size (in raw frames).
        kwargs: optional caller kwargs — if it contains `"cu_seqlens"` it is popped and returned.

    Returns:
        `(num_windows + 1,)` int32 cumulative sequence boundaries.
    """
    if kwargs is not None and (cu_seqlens := kwargs.pop("cu_seqlens", None)) is not None:
        return cu_seqlens

    aftercnn_lens = _get_feat_extract_output_lengths(feature_lens)
    feature_lens_after_cnn = _get_feat_extract_output_lengths(chunk_lengths)
    max_len_after_cnn = feature_lens_after_cnn.max().item()

    n_window_ratio = n_window_infer // (n_window * 2)
    window_aftercnn = max_len_after_cnn * n_window_ratio

    cu_chunk_lens = [0]
    for cnn_len in aftercnn_lens:
        cu_chunk_lens += [window_aftercnn] * (cnn_len // window_aftercnn)
        remainder = cnn_len % window_aftercnn
        if remainder != 0:
            cu_chunk_lens += [remainder]

    return torch.tensor(cu_chunk_lens, device=feature_lens.device).cumsum(-1, dtype=torch.int32)


def get_audio_cu_seqlens(
    chunk_lengths: torch.Tensor,
    feature_lens: torch.Tensor,
    n_window_infer: int,
    n_window: int,
    kwargs: dict | None = None,
) -> torch.Tensor:
    """Compute cumulative sequence lengths for audio attention windowing, or pop `"cu_seqlens"` from `kwargs` if precomputed.

    Splits each sample's post-CNN features into inference windows and returns
    cumulative boundaries for flash-attention-style sequence packing.

    Args:
        chunk_lengths: `(num_chunks,)` pre-CNN chunk lengths.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window_infer: inference window size (in raw frames).
        n_window: half the chunk size (in raw frames).
        kwargs: optional caller kwargs — if it contains `"cu_seqlens"` it is popped and returned.

    Returns:
        `(num_windows + 1,)` int32 cumulative sequence boundaries.
    """
    if kwargs is not None and (cu_seqlens := kwargs.pop("cu_seqlens", None)) is not None:
        return cu_seqlens

    aftercnn_lens = _get_feat_extract_output_lengths(feature_lens)
    feature_lens_after_cnn = _get_feat_extract_output_lengths(chunk_lengths)
    max_len_after_cnn = feature_lens_after_cnn.max().item()

    n_window_ratio = n_window_infer // (n_window * 2)
    window_aftercnn = max_len_after_cnn * n_window_ratio

    cu_chunk_lens = [0]
    for cnn_len in aftercnn_lens:
        cu_chunk_lens += [window_aftercnn] * (cnn_len // window_aftercnn)
        remainder = cnn_len % window_aftercnn
        if remainder != 0:
            cu_chunk_lens += [remainder]

    return torch.tensor(cu_chunk_lens, device=feature_lens.device).cumsum(-1, dtype=torch.int32)

