
def get_position_ids(attention_mask: torch.Tensor, use_past_kv: bool):
    position_ids = attention_mask.long().cumsum(-1) - 1
    position_ids.masked_fill_(attention_mask == 0, 1)
    if use_past_kv:
        # Shape: (batch_size, 1)
        position_ids = position_ids[:, -1].unsqueeze(-1)

    # Shape: (batch_size, sequence_length)
    return position_ids

