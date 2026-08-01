
def concat_padded_sequences(seq1, mask1, seq2, mask2, return_index: bool = False):
    """
    Concatenates two right-padded sequences, such that the resulting sequence
    is contiguous and also right-padded.

    Tensors are batch-first, masks are batch-first with True=valid, False=padding.

    Args:
        seq1: A tensor of shape (batch_size, seq1_length, hidden_size).
        mask1: A tensor of shape (batch_size, seq1_length) with True=valid, False=padding.
        seq2: A tensor of shape (batch_size, seq2_length, hidden_size).
        mask2: A tensor of shape (batch_size, seq2_length) with True=valid, False=padding.
        return_index: If True, also returns the index of the ids of the element of seq2
            in the concatenated sequence. This can be used to retrieve the elements of seq2.

    Returns:
        A tuple (concatenated_sequence, concatenated_mask) if return_index is False,
        otherwise (concatenated_sequence, concatenated_mask, index).
        The concatenated_mask uses True=valid, False=padding convention.
    """
    batch_size, seq1_length, hidden_size = seq1.shape
    batch_size2, seq2_length, hidden_size2 = seq2.shape

    assert batch_size == batch_size2 == mask1.size(0) == mask2.size(0)
    assert hidden_size == hidden_size2
    assert seq1_length == mask1.size(1)
    assert seq2_length == mask2.size(1)

    actual_seq1_lengths = mask1.sum(dim=-1)
    actual_seq2_lengths = mask2.sum(dim=-1)

    final_lengths = actual_seq1_lengths + actual_seq2_lengths
    max_length = seq1_length + seq2_length

    concatenated_mask = (
        torch.arange(max_length, device=seq2.device)[None].repeat(batch_size, 1) < final_lengths[:, None]
    )

    concatenated_sequence = torch.zeros((batch_size, max_length, hidden_size), device=seq2.device, dtype=seq2.dtype)
    concatenated_sequence[:, :seq1_length, :] = seq1

    # Shift seq2 elements to start at the end of valid seq1
    index = torch.arange(seq2_length, device=seq2.device)[None].repeat(batch_size, 1)
    index = index + actual_seq1_lengths[:, None]

    # Scatter seq2 into the right positions
    concatenated_sequence = concatenated_sequence.scatter(1, index[:, :, None].expand(-1, -1, hidden_size), seq2)

    if return_index:
        return concatenated_sequence, concatenated_mask, index

    return concatenated_sequence, concatenated_mask


def concat_padded_sequences(seq1, mask1, seq2, mask2, return_index: bool = False):
    """
    Concatenates two right-padded sequences, such that the resulting sequence
    is contiguous and also right-padded.

    Tensors are batch-first, masks are batch-first with True=valid, False=padding.

    Args:
        seq1: A tensor of shape (batch_size, seq1_length, hidden_size).
        mask1: A tensor of shape (batch_size, seq1_length) with True=valid, False=padding.
        seq2: A tensor of shape (batch_size, seq2_length, hidden_size).
        mask2: A tensor of shape (batch_size, seq2_length) with True=valid, False=padding.
        return_index: If True, also returns the index of the ids of the element of seq2
            in the concatenated sequence. This can be used to retrieve the elements of seq2.

    Returns:
        A tuple (concatenated_sequence, concatenated_mask) if return_index is False,
        otherwise (concatenated_sequence, concatenated_mask, index).
        The concatenated_mask uses True=valid, False=padding convention.
    """
    batch_size, seq1_length, hidden_size = seq1.shape
    batch_size2, seq2_length, hidden_size2 = seq2.shape

    assert batch_size == batch_size2 == mask1.size(0) == mask2.size(0)
    assert hidden_size == hidden_size2
    assert seq1_length == mask1.size(1)
    assert seq2_length == mask2.size(1)

    actual_seq1_lengths = mask1.sum(dim=-1)
    actual_seq2_lengths = mask2.sum(dim=-1)

    final_lengths = actual_seq1_lengths + actual_seq2_lengths
    max_length = seq1_length + seq2_length

    concatenated_mask = (
        torch.arange(max_length, device=seq2.device)[None].repeat(batch_size, 1) < final_lengths[:, None]
    )

    concatenated_sequence = torch.zeros((batch_size, max_length, hidden_size), device=seq2.device, dtype=seq2.dtype)
    concatenated_sequence[:, :seq1_length, :] = seq1

    # Shift seq2 elements to start at the end of valid seq1
    index = torch.arange(seq2_length, device=seq2.device)[None].repeat(batch_size, 1)
    index = index + actual_seq1_lengths[:, None]

    # Scatter seq2 into the right positions
    concatenated_sequence = concatenated_sequence.scatter(1, index[:, :, None].expand(-1, -1, hidden_size), seq2)

    if return_index:
        return concatenated_sequence, concatenated_mask, index

    return concatenated_sequence, concatenated_mask

