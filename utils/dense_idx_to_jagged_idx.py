
def dense_idx_to_jagged_idx(batch_idx, seq_idx, offsets_loader, jagged_len):
    # jagged_len + 1 is used as the upper bound,
    # because the last sequence length may be zero
    begin_idx = ops.indirect_indexing(
        offsets_loader([batch_idx]),
        jagged_len + 1,
    )
    end_idx = offsets_loader([batch_idx + 1])
    jagged_idx = begin_idx + seq_idx
    return jagged_idx, end_idx

