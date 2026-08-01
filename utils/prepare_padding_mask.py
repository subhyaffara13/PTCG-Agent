
def prepare_padding_mask(attention_mask: torch.Tensor | None, kv_length: int, kv_offset: int) -> torch.Tensor | None:
    """
    From the 2D attention mask, prepare the correct padding mask to use by potentially padding it.
    """
    local_padding_mask = attention_mask
    if attention_mask is not None:
        # Pad it if necessary
        if (padding_length := kv_length + kv_offset - attention_mask.shape[-1]) > 0:
            local_padding_mask = torch.nn.functional.pad(attention_mask, (0, padding_length))
    return local_padding_mask

