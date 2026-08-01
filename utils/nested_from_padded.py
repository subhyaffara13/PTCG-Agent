
def nested_from_padded(
    padded, offsets, ragged_idx=1, min_seqlen=None, max_seqlen=None, sum_S=None
):
    min_seqlen_tensor = None
    if min_seqlen is not None:
        min_seqlen_tensor = _store_val_in_tensor(min_seqlen)

    max_seqlen_tensor = None
    if max_seqlen is not None:
        max_seqlen_tensor = _store_val_in_tensor(max_seqlen)

    return torch._nested_from_padded_tensor(
        padded,
        offsets,
        _nt_view_dummy(),
        ragged_idx,
        min_seqlen_tensor,
        max_seqlen_tensor,
        sum_S,
    )

