
def make_default_2d_attention_mask(
    token_ids: torch.LongTensor | None,
    hidden_states: torch.Tensor,
    pad_token_id: int | None,
) -> torch.Tensor:
    """Construct the default attention mask."""
    if token_ids is not None:
        if pad_token_id is None:
            raise ValueError("`pad_token_id` is required for padding information.")
        attention_mask = (token_ids != pad_token_id).to(hidden_states.device, torch.long)
    else:
        attention_mask = torch.ones(
            (hidden_states.shape[0], hidden_states.shape[1]), device=hidden_states.device, dtype=torch.long
        )
    return attention_mask


def make_default_2d_attention_mask(
    token_ids: torch.LongTensor | None,
    hidden_states: torch.Tensor,
    pad_token_id: int | None,
) -> torch.Tensor:
    """Construct the default attention mask."""
    if token_ids is not None:
        if pad_token_id is None:
            raise ValueError("`pad_token_id` is required for padding information.")
        attention_mask = (token_ids != pad_token_id).to(hidden_states.device, torch.long)
    else:
        attention_mask = torch.ones(
            (hidden_states.shape[0], hidden_states.shape[1]), device=hidden_states.device, dtype=torch.long
        )
    return attention_mask

