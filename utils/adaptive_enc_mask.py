
def adaptive_enc_mask(x_len, chunk_start_idx, left_window=0, right_window=0):
    """
    The function is very important for Transformer Transducer Streaming mode
    Args:
        xs_len (int): sequence length
        chunk_start_idx (list): first idx of each chunk, such as [0,18,36,48]. It also supports adaptive chunk size [0,10,15,45]
        left_window (int): how many left chunks can be seen
        right_window (int): how many right chunks can be seen. It is used for chunk overlap model.
        Returns:
            mask (torch.Tensor): a mask tensor for streaming model
    """
    chunk_start_idx = torch.Tensor(chunk_start_idx).long()
    start_pad = torch.nn.functional.pad(
        chunk_start_idx, (1, 0)
    )  # append 0 to the beginning, so it becomes [0, 0, 18, 36, 48]
    end_pad = torch.nn.functional.pad(
        chunk_start_idx, (0, 1), value=x_len
    )  # append x_len to the end, so it becomes [0,18,36,48, x_len]
    seq_range = torch.arange(0, x_len).unsqueeze(-1)
    idx = ((seq_range < end_pad) & (seq_range >= start_pad)).nonzero()[:, 1]
    seq_range_expand = torch.arange(0, x_len).unsqueeze(0).expand(x_len, -1)
    idx_left = idx - left_window
    idx_left[idx_left < 0] = 0
    boundary_left = start_pad[idx_left]
    mask_left = seq_range_expand >= boundary_left.unsqueeze(-1)
    idx_right = idx + right_window
    idx_right[idx_right > len(chunk_start_idx)] = len(chunk_start_idx)
    boundary_right = end_pad[idx_right]
    mask_right = seq_range_expand < boundary_right.unsqueeze(-1)
    return mask_left & mask_right


def adaptive_enc_mask(x_len, chunk_start_idx, left_window=0, right_window=0):
    """
    The function is very important for Transformer Transducer Streaming mode
    Args:
        xs_len (int): sequence length
        chunk_start_idx (list): first idx of each chunk, such as [0,18,36,48]. It also supports adaptive chunk size [0,10,15,45]
        left_window (int): how many left chunks can be seen
        right_window (int): how many right chunks can be seen. It is used for chunk overlap model.
        Returns:
            mask (torch.Tensor): a mask tensor for streaming model
    """
    chunk_start_idx = torch.Tensor(chunk_start_idx).long()
    start_pad = torch.nn.functional.pad(
        chunk_start_idx, (1, 0)
    )  # append 0 to the beginning, so it becomes [0, 0, 18, 36, 48]
    end_pad = torch.nn.functional.pad(
        chunk_start_idx, (0, 1), value=x_len
    )  # append x_len to the end, so it becomes [0,18,36,48, x_len]
    seq_range = torch.arange(0, x_len).unsqueeze(-1)
    idx = ((seq_range < end_pad) & (seq_range >= start_pad)).nonzero()[:, 1]
    seq_range_expand = torch.arange(0, x_len).unsqueeze(0).expand(x_len, -1)
    idx_left = idx - left_window
    idx_left[idx_left < 0] = 0
    boundary_left = start_pad[idx_left]
    mask_left = seq_range_expand >= boundary_left.unsqueeze(-1)
    idx_right = idx + right_window
    idx_right[idx_right > len(chunk_start_idx)] = len(chunk_start_idx)
    boundary_right = end_pad[idx_right]
    mask_right = seq_range_expand < boundary_right.unsqueeze(-1)
    return mask_left & mask_right

