from typing import Callable

def flex_attention_mask(
    batch_size: int,
    q_length: int,
    kv_length: int,
    q_offset: int = 0,
    kv_offset: int = 0,
    mask_function: Callable = causal_mask_function,
    attention_mask: torch.Tensor | None = None,
    device: torch.device | str = "cpu",
    **kwargs,
) -> BlockMask:
    """
    Create a 4D block mask which is a compressed representation of the full 4D block causal mask. BlockMask is essential
    for performant computation of flex attention. See: https://pytorch.org/blog/flexattention/

    Args:
        batch_size (`int`):
            The batch size of the input sequence.
        q_length (`int`):
            The size that the query states will have during the attention computation.
        kv_length (`int`):
            The size that the key and value states will have during the attention computation.
        q_offset (`int`, optional):
            An optional offset to indicate at which first position the query states will refer to.
        kv_offset (`int`, optional):
            An optional offset to indicate at which first position the key and values states will refer to.
        mask_function (`Callable`):
            The mask factory function describing the mask pattern.
        attention_mask (`torch.Tensor`, optional):
            The 2D attention mask corresponding to padded tokens of shape (batch_size, number_of_seen_tokens+q_length)
        device (`torch.device` or `str`, optional):
            An optional device to create the mask on.
    """
    # Potentially add the padding 2D mask
    if attention_mask is not None:
        # Older torch (2.5.x) cannot handle sequences not in multiples of 128 (default block size)
        # Hence we pad to multiples of this as a minimum to ensure this
        pad_len = ((attention_mask.shape[1] // flex_default_block_size) + 1) * flex_default_block_size
        pad_len = pad_len - attention_mask.shape[1]
        if not _is_torch_greater_or_equal_than_2_6 and pad_len > 0:
            attention_mask = torch.nn.functional.pad(attention_mask, value=0, pad=(0, pad_len))

        padding_mask = prepare_padding_mask(attention_mask, kv_length, kv_offset)
        mask_function = and_masks(mask_function, padding_mask_function(padding_mask))

    # Add the offsets on top (because flex interface only allows length, not start and end indices)
    mask_function = add_offsets_to_mask_function(mask_function, q_offset, kv_offset)

    # Finally create the block mask
    block_mask = create_block_mask(
        mask_mod=mask_function,
        B=batch_size,
        H=None,
        Q_LEN=q_length,
        KV_LEN=kv_length,
        device=device,
        _compile=_is_torch_greater_or_equal_than_2_6,
    )
    return block_mask

