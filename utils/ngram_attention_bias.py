
def ngram_attention_bias(sequence_length, ngram, device, dtype):
    """
    This function computes the bias for the predict stream
    """
    left_block = (
        torch.ones((ngram, sequence_length, sequence_length), device=device, dtype=dtype) * torch.finfo(dtype).min
    )
    right_block = left_block.detach().clone()
    # create bias
    for stream_idx in range(ngram):
        right_block[stream_idx].fill_diagonal_(0, wrap=False)
        left_block[stream_idx].triu_(-stream_idx + 1)

    left_block[:, :, 0] = 0
    return torch.cat([left_block, right_block], dim=2)

