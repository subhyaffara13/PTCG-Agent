
def chunk_and_pad_features(
    input_features: torch.Tensor, feature_lens: torch.Tensor, n_window: int, kwargs: dict | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Split audio features into fixed-size chunks and pad to uniform length, or pop precomputed pair from `kwargs`.

    Each audio sample is split into chunks of `n_window * 2` frames (the last
    chunk may be shorter), then all chunks are right-padded to the longest chunk.

    Args:
        input_features: `(feature_dim, total_frames)` concatenated audio features.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window: half the target chunk size in frames.
        kwargs: optional caller kwargs — if it contains both `"padded_feature"` and `"chunk_lengths"` they are popped and returned.

    Returns:
        `padded_feature`: `(num_chunks, feature_dim, max_chunk_len)` padded chunks.
        `chunk_lengths`: `(num_chunks,)` actual length of each chunk before padding.
    """
    if kwargs is not None:
        padded_feature = kwargs.pop("padded_feature", None)
        chunk_lengths = kwargs.pop("chunk_lengths", None)
        if padded_feature is not None and chunk_lengths is not None:
            return padded_feature, chunk_lengths

    chunk_num = torch.ceil(feature_lens / (n_window * 2)).long()
    chunk_lengths = torch.full((chunk_num.sum(),), n_window * 2, dtype=torch.long, device=feature_lens.device)
    tail_chunk_index = F.pad(chunk_num, (1, 0), value=-1).cumsum(0)[1:]
    chunk_lengths[tail_chunk_index] = feature_lens % (n_window * 2)
    chunk_lengths = torch.where(chunk_lengths == 0, n_window * 2, chunk_lengths)

    chunk_list = input_features.T.split(chunk_lengths.tolist(), dim=0)
    padded_feature = nn.utils.rnn.pad_sequence(chunk_list, batch_first=True).transpose(1, 2)
    return padded_feature, chunk_lengths


def chunk_and_pad_features(
    input_features: torch.Tensor, feature_lens: torch.Tensor, n_window: int, kwargs: dict | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Split audio features into fixed-size chunks and pad to uniform length, or pop precomputed pair from `kwargs`.

    Each audio sample is split into chunks of `n_window * 2` frames (the last
    chunk may be shorter), then all chunks are right-padded to the longest chunk.

    Args:
        input_features: `(feature_dim, total_frames)` concatenated audio features.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window: half the target chunk size in frames.
        kwargs: optional caller kwargs — if it contains both `"padded_feature"` and `"chunk_lengths"` they are popped and returned.

    Returns:
        `padded_feature`: `(num_chunks, feature_dim, max_chunk_len)` padded chunks.
        `chunk_lengths`: `(num_chunks,)` actual length of each chunk before padding.
    """
    if kwargs is not None:
        padded_feature = kwargs.pop("padded_feature", None)
        chunk_lengths = kwargs.pop("chunk_lengths", None)
        if padded_feature is not None and chunk_lengths is not None:
            return padded_feature, chunk_lengths

    chunk_num = torch.ceil(feature_lens / (n_window * 2)).long()
    chunk_lengths = torch.full((chunk_num.sum(),), n_window * 2, dtype=torch.long, device=feature_lens.device)
    tail_chunk_index = F.pad(chunk_num, (1, 0), value=-1).cumsum(0)[1:]
    chunk_lengths[tail_chunk_index] = feature_lens % (n_window * 2)
    chunk_lengths = torch.where(chunk_lengths == 0, n_window * 2, chunk_lengths)

    chunk_list = input_features.T.split(chunk_lengths.tolist(), dim=0)
    padded_feature = nn.utils.rnn.pad_sequence(chunk_list, batch_first=True).transpose(1, 2)
    return padded_feature, chunk_lengths


def chunk_and_pad_features(
    input_features: torch.Tensor, feature_lens: torch.Tensor, n_window: int, kwargs: dict | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Split audio features into fixed-size chunks and pad to uniform length, or pop precomputed pair from `kwargs`.

    Each audio sample is split into chunks of `n_window * 2` frames (the last
    chunk may be shorter), then all chunks are right-padded to the longest chunk.

    Args:
        input_features: `(feature_dim, total_frames)` concatenated audio features.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window: half the target chunk size in frames.
        kwargs: optional caller kwargs — if it contains both `"padded_feature"` and `"chunk_lengths"` they are popped and returned.

    Returns:
        `padded_feature`: `(num_chunks, feature_dim, max_chunk_len)` padded chunks.
        `chunk_lengths`: `(num_chunks,)` actual length of each chunk before padding.
    """
    if kwargs is not None:
        padded_feature = kwargs.pop("padded_feature", None)
        chunk_lengths = kwargs.pop("chunk_lengths", None)
        if padded_feature is not None and chunk_lengths is not None:
            return padded_feature, chunk_lengths

    chunk_num = torch.ceil(feature_lens / (n_window * 2)).long()
    chunk_lengths = torch.full((chunk_num.sum(),), n_window * 2, dtype=torch.long, device=feature_lens.device)
    tail_chunk_index = F.pad(chunk_num, (1, 0), value=-1).cumsum(0)[1:]
    chunk_lengths[tail_chunk_index] = feature_lens % (n_window * 2)
    chunk_lengths = torch.where(chunk_lengths == 0, n_window * 2, chunk_lengths)

    chunk_list = input_features.T.split(chunk_lengths.tolist(), dim=0)
    padded_feature = nn.utils.rnn.pad_sequence(chunk_list, batch_first=True).transpose(1, 2)
    return padded_feature, chunk_lengths


def chunk_and_pad_features(
    input_features: torch.Tensor, feature_lens: torch.Tensor, n_window: int, kwargs: dict | None = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """Split audio features into fixed-size chunks and pad to uniform length, or pop precomputed pair from `kwargs`.

    Each audio sample is split into chunks of `n_window * 2` frames (the last
    chunk may be shorter), then all chunks are right-padded to the longest chunk.

    Args:
        input_features: `(feature_dim, total_frames)` concatenated audio features.
        feature_lens: `(batch_size,)` per-sample frame counts.
        n_window: half the target chunk size in frames.
        kwargs: optional caller kwargs — if it contains both `"padded_feature"` and `"chunk_lengths"` they are popped and returned.

    Returns:
        `padded_feature`: `(num_chunks, feature_dim, max_chunk_len)` padded chunks.
        `chunk_lengths`: `(num_chunks,)` actual length of each chunk before padding.
    """
    if kwargs is not None:
        padded_feature = kwargs.pop("padded_feature", None)
        chunk_lengths = kwargs.pop("chunk_lengths", None)
        if padded_feature is not None and chunk_lengths is not None:
            return padded_feature, chunk_lengths

    chunk_num = torch.ceil(feature_lens / (n_window * 2)).long()
    chunk_lengths = torch.full((chunk_num.sum(),), n_window * 2, dtype=torch.long, device=feature_lens.device)
    tail_chunk_index = F.pad(chunk_num, (1, 0), value=-1).cumsum(0)[1:]
    chunk_lengths[tail_chunk_index] = feature_lens % (n_window * 2)
    chunk_lengths = torch.where(chunk_lengths == 0, n_window * 2, chunk_lengths)

    chunk_list = input_features.T.split(chunk_lengths.tolist(), dim=0)
    padded_feature = nn.utils.rnn.pad_sequence(chunk_list, batch_first=True).transpose(1, 2)
    return padded_feature, chunk_lengths

