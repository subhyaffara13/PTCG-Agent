
def create_masks_for_generate(
    config: PreTrainedConfig,
    inputs_embeds: torch.Tensor,
    attention_mask: torch.Tensor | None,
    past_key_values: Cache | None,
    position_ids: torch.Tensor | None = None,
    or_mask_function: Callable | None = None,
    and_mask_function: Callable | None = None,
    block_sequence_ids: torch.Tensor | None = None,
    **kwargs,
):
    """
    This function mimics how we create the masks in the `modeling_xxx.py` files, and is used in places like `generate`
    in order to easily create the masks in advance, when we compile the forwards with Static caches.

    Args:
        config (`PreTrainedConfig`):
            The model config.
        inputs_embeds (`torch.Tensor`):
            The input embeddings of shape (batch_size, query_length, hidden_dim). This is used only to infer the
            batch size, query length and dtype.
        attention_mask (`torch.Tensor`, optional):
            The 2D attention mask corresponding to padded tokens of shape (batch_size, number_of_seen_tokens+q_length).
            It can also be an already prepared 4D mask, in which case it is returned as-is.
        past_key_values (`Cache`, optional):
            The past key values, if we use a cache.
        position_ids (`torch.Tensor`, optional)
            A 2D tensor of shape (batch_size, query_length) indicating the positions of each token in the sequences.
        or_mask_function (`Callable`, optional):
            An optional mask function to combine with the other mask function (by doing the union of both). This is
            useful to easily overlay another mask on top of the causal one, for example for image tokens handling.
        and_mask_function (`Callable`, optional):
            An optional mask function to combine with the other mask function (by doing the intersection of both). This is
            useful to easily overlay another mask on top of the causal one, for example for image tokens handling.
        block_sequence_ids (`torch.Tensor`, *optional*):
            A tensor of same shape as input IDs indicating to which block or group each token belongs to. Tokens from
            the same block will keep a bidirectional mask within the block, attending causally to the past. Index `-1`
            can be used for blocks that have to keep complete causality within itself.
    """
    # The attribute reside in the text config for composite models
    effective_config = config.get_text_config()
    # Prepare the mask args
    mask_kwargs = {
        "config": effective_config,
        "inputs_embeds": inputs_embeds,
        "attention_mask": attention_mask,
        "past_key_values": past_key_values,
        "position_ids": position_ids,
        "or_mask_function": or_mask_function,
        "and_mask_function": and_mask_function,
        "block_sequence_ids": block_sequence_ids,
    }

    # If the attribute exist, we need several masks - unless every layer shares the same type, in which
    # case we return a single mask.
    if hasattr(effective_config, "layer_types"):
        layer_patterns = set(effective_config.layer_types)
        if len(layer_patterns) == 1:
            return LAYER_PATTERN_TO_MASK_FUNCTION_MAPPING[next(iter(layer_patterns))](**mask_kwargs)
        causal_masks = {}
        for layer_pattern in layer_patterns:
            causal_masks[layer_pattern] = LAYER_PATTERN_TO_MASK_FUNCTION_MAPPING[layer_pattern](**mask_kwargs)
        return causal_masks
    # In this case, all layers are sliding
    elif getattr(effective_config, "sliding_window", None) is not None:
        return create_sliding_window_causal_mask(**mask_kwargs)
    # In this case, all layers are chunked
    elif getattr(effective_config, "attention_chunk_size", None) is not None:
        return create_chunked_causal_mask(**mask_kwargs)
    # All layers use standard causal attention
    return create_causal_mask(**mask_kwargs)

