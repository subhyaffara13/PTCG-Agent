
def unfold_tensor(tensor, max_seq_len):
    """
    For a given tensor with shape of (N, T, D), if sequence length T is longer than max_seq_len,
    this function unfold it to a (NT', max_seq_len, D) where T' is T // max_seq_len.
    Args:
        tensor: N, T, D
    """
    _, _, D = tensor.shape
    tensor = tensor.transpose(-1, -2)
    # N x D x 1 x T => N x (D x max_seq_len) x T'
    tensor = F.unfold(tensor[..., None, :], kernel_size=(1, max_seq_len), stride=(1, max_seq_len))

    new_bsz, _, slen = tensor.shape
    tensor = tensor.view(new_bsz, -1, max_seq_len, slen)
    tensor = tensor.permute(0, 3, 2, 1)
    tensor = tensor.view(-1, max_seq_len, D).contiguous()
    return tensor


def unfold_tensor(tensor, max_seq_len):
    """
    For a given tensor with shape of (N, T, D), if sequence length T is longer than max_seq_len,
    this function unfold it to a (NT', max_seq_len, D) where T' is T // max_seq_len.
    Args:
        tensor: N, T, D
    """
    _, _, D = tensor.shape
    tensor = tensor.transpose(-1, -2)
    # N x D x 1 x T => N x (D x max_seq_len) x T'
    tensor = F.unfold(tensor[..., None, :], kernel_size=(1, max_seq_len), stride=(1, max_seq_len))

    new_bsz, _, slen = tensor.shape
    tensor = tensor.view(new_bsz, -1, max_seq_len, slen)
    tensor = tensor.permute(0, 3, 2, 1)
    tensor = tensor.view(-1, max_seq_len, D).contiguous()
    return tensor

