
def _cumulative_and_max_seq_len_nnz(qkv: torch.Tensor) -> tuple[torch.Tensor, int, int]:
    # This function is used to calculate two pieces of metadata that are needed
    # for use with flash-attention and efficient_attention kernels. They are the
    # cumulative sequence_length over a batch of sequences and the maximum
    # sequence length.

    # It returns a tuple of cumulative sequence lengths and the maximum sequence
    # length, and the last element in the cumulative_sequence_lengths
    if not isinstance(qkv, NestedTensor):
        raise ValueError("QKV must be nested for flash cumulative_seq_len calculation.")

    if qkv.lengths() is None:
        # TODO: Explore performance impact of copying
        cumulative_seqlen = qkv.offsets().to(dtype=torch.int32, device=qkv.device)
        max_seqlen = qkv._get_max_seqlen()
        n_elem = qkv.values().shape[0]
    else:
        # TODO: Explore performance impact of copying
        cumulative_seqlen = (
            qkv.lengths().cumsum(0).to(dtype=torch.int32, device=qkv.device)
        )
        max_seqlen = qkv._get_max_seqlen()
        # TODO: Explore performance impact when compiling
        n_elem = int(cumulative_seqlen[-1].item())
    return cumulative_seqlen, max_seqlen, n_elem

