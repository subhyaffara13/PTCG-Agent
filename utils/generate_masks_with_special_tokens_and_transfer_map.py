
def generate_masks_with_special_tokens_and_transfer_map(input_ids: torch.LongTensor) -> tuple[Tensor, Tensor]:
    """Generate attention mask between each pair of special tokens and positional ids.
    Args:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            Indices of input sequence tokens in the vocabulary.
    Returns:
        `tuple(torch.Tensor)` comprising attention mask between each special tokens and position_ids:
        - **attention_mask** (`torch.BoolTensor` of shape `(batch_size, sequence_length, sequence_length)`)
        - **position_ids** (`torch.LongTensor` of shape `(batch_size, sequence_length)`)
    """
    batch_size, seq_len = input_ids.shape
    device = input_ids.device

    # Identify special token positions
    special_mask = torch.isin(input_ids, torch.tensor(SPECIAL_TOKENS, device=device))

    # For each position, find the previous and next special token indices
    indices = torch.arange(seq_len, device=device).unsqueeze(0).expand(batch_size, -1)

    # Previous special token: cummax of special token indices
    prev_special = torch.where(special_mask, indices, torch.tensor(-1, device=device))
    prev_special = torch.cummax(prev_special, dim=1)[0]

    # Next special token: flip, cummin, flip back
    next_special = torch.where(special_mask, indices, torch.tensor(seq_len, device=device))
    next_special = torch.flip(torch.cummin(torch.flip(next_special, dims=[1]), dim=1)[0], dims=[1])

    # Tokens with the same next_special belong to the same block
    # Exclude blocks whose closing delimiter is at position 0 or seq_len-1
    valid_block = (next_special != 0) & (next_special != seq_len - 1) & (next_special != seq_len)

    # Build attention mask: tokens attend to each other if they share the same next_special
    next_i = next_special.unsqueeze(2)  # (B, N, 1)
    next_j = next_special.unsqueeze(1)  # (B, 1, N)
    attention_mask = (next_i == next_j) & valid_block.unsqueeze(1)

    # Always allow self-attention
    identity = torch.eye(seq_len, device=device, dtype=torch.bool).unsqueeze(0).expand(batch_size, -1, -1)
    attention_mask = identity | attention_mask

    # Position IDs: distance from previous special token
    position_ids = indices - prev_special - 1
    position_ids = torch.where(valid_block, position_ids, torch.zeros_like(position_ids))
    position_ids = torch.clamp(position_ids, min=0).to(torch.long)

    return attention_mask, position_ids


def generate_masks_with_special_tokens_and_transfer_map(input_ids: torch.LongTensor) -> tuple[Tensor, Tensor]:
    """Generate attention mask between each pair of special tokens and positional ids.
    Args:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            Indices of input sequence tokens in the vocabulary.
    Returns:
        `tuple(torch.Tensor)` comprising attention mask between each special tokens and position_ids:
        - **attention_mask** (`torch.BoolTensor` of shape `(batch_size, sequence_length, sequence_length)`)
        - **position_ids** (`torch.LongTensor` of shape `(batch_size, sequence_length)`)
    """
    batch_size, seq_len = input_ids.shape
    device = input_ids.device

    # Identify special token positions
    special_mask = torch.isin(input_ids, torch.tensor(SPECIAL_TOKENS, device=device))

    # For each position, find the previous and next special token indices
    indices = torch.arange(seq_len, device=device).unsqueeze(0).expand(batch_size, -1)

    # Previous special token: cummax of special token indices
    prev_special = torch.where(special_mask, indices, torch.tensor(-1, device=device))
    prev_special = torch.cummax(prev_special, dim=1)[0]

    # Next special token: flip, cummin, flip back
    next_special = torch.where(special_mask, indices, torch.tensor(seq_len, device=device))
    next_special = torch.flip(torch.cummin(torch.flip(next_special, dims=[1]), dim=1)[0], dims=[1])

    # Tokens with the same next_special belong to the same block
    # Exclude blocks whose closing delimiter is at position 0 or seq_len-1
    valid_block = (next_special != 0) & (next_special != seq_len - 1) & (next_special != seq_len)

    # Build attention mask: tokens attend to each other if they share the same next_special
    next_i = next_special.unsqueeze(2)  # (B, N, 1)
    next_j = next_special.unsqueeze(1)  # (B, 1, N)
    attention_mask = (next_i == next_j) & valid_block.unsqueeze(1)

    # Always allow self-attention
    identity = torch.eye(seq_len, device=device, dtype=torch.bool).unsqueeze(0).expand(batch_size, -1, -1)
    attention_mask = identity | attention_mask

    # Position IDs: distance from previous special token
    position_ids = indices - prev_special - 1
    position_ids = torch.where(valid_block, position_ids, torch.zeros_like(position_ids))
    position_ids = torch.clamp(position_ids, min=0).to(torch.long)

    return attention_mask, position_ids

