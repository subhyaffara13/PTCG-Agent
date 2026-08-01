
def create_bidirectional_mask(
    config: PreTrainedConfig,
    inputs_embeds: torch.Tensor,
    attention_mask: torch.Tensor | None,
    encoder_hidden_states: torch.Tensor | None = None,
    past_key_values: Cache | None = None,
    or_mask_function: Callable | None = None,
    and_mask_function: Callable | None = None,
    **kwargs,
) -> torch.Tensor | BlockMask | None:
    """
    Create a standard bidirectional mask based on the attention implementation used (stored in the config).

    Args:
        config (`PreTrainedConfig`):
            The model config.
        inputs_embeds (`torch.Tensor`):
            The input embeddings of shape (batch_size, query_length, hidden_dim). This is only used to infer metadata
            such as the batch size, query length, dtype, and device.
        attention_mask (`torch.Tensor`, optional):
            The 2D attention mask corresponding to padded tokens of shape (batch_size, kv_length).
            It can also be an already prepared 4D mask of shape (batch_size, 1, query_length, kv_length),
            in which case it is returned as-is.
        encoder_hidden_states (`torch.Tensor`, optional):
            The input embeddings of shape (batch_size, kv_length, hidden_dim). If provided, it is used instead of
            `inputs_embeds` to infer the batch size, kv length and dtype.
        past_key_values (`Cache`, optional):
            The past key values, if we use a cache.
        or_mask_function (`Callable`, optional):
            An optional mask function to combine with the base mask function (by doing the union of both). This is
            useful to easily overlay another mask on top, for example for image tokens handling.
        and_mask_function (`Callable`, optional):
            An optional mask function to combine with the base mask function (by doing the intersection of both). This is
            useful to easily overlay another mask on top, for example for image tokens handling.
    """
    # If we have an hybrid cache structure, here we want to create the mask for the full layers
    if hasattr(past_key_values, "is_sliding") and False in past_key_values.is_sliding:
        layer_idx = past_key_values.is_sliding.index(False)
    else:
        layer_idx = 0

    # We ignore a few irrelevant arguments at the end as we do not have a (growing) cache here
    early_exit, attention_mask, _, q_length, kv_length, q_offset, kv_offset = _preprocess_mask_arguments(
        config, inputs_embeds, attention_mask, past_key_values, None, layer_idx, encoder_hidden_states
    )
    if early_exit:
        return attention_mask

    embeds = encoder_hidden_states if encoder_hidden_states is not None else inputs_embeds
    batch_size, dtype = embeds.shape[0], embeds.dtype
    # Use `inputs_embeds.device` to stay consistent with `_preprocess_mask_arguments`, which moves the 2D
    # `attention_mask` to that device. In model parallel setups, `encoder_hidden_states` may live on a different
    # device than `inputs_embeds` (e.g. cross-attention from a decoder to encoder states).
    device = inputs_embeds.device
    mask_factory_function = bidirectional_mask_function
    mask_interface = ALL_MASK_ATTENTION_FUNCTIONS[config._attn_implementation]

    # Allow skipping the mask creation except we have additional masking operators (and/or masks)
    allow_is_bidirectional_skip = True
    # Defaulting to using non-vmap based mask creations except when detecting
    # users passing custom mask functions (as we cannot guarantee that they
    # are properly index-based as required by our implementation).
    use_vmap = False

    # Allow slight deviations from the base mask
    # Note that it is very important to apply this before any other deviations of the mask (such as packed sequence mask,
    # padding mask, etc) as the resulting mask may otherwise not be correct!
    if or_mask_function is not None:
        if not _is_torch_greater_or_equal_than_2_6:
            raise ValueError("Using `or_mask_function` or `and_mask_function` arguments require torch>=2.6")
        mask_factory_function = or_masks(mask_factory_function, or_mask_function)
        allow_is_bidirectional_skip = False
        use_vmap = True
    if and_mask_function is not None:
        if not _is_torch_greater_or_equal_than_2_6:
            raise ValueError("Using `or_mask_function` or `and_mask_function` arguments require torch>=2.6")
        mask_factory_function = and_masks(mask_factory_function, and_mask_function)
        allow_is_bidirectional_skip = False
        use_vmap = True

    # We now create the mask
    attention_mask = mask_interface(
        batch_size=batch_size,
        q_length=q_length,
        kv_length=kv_length,
        q_offset=q_offset,
        kv_offset=kv_offset,
        mask_function=mask_factory_function,
        attention_mask=attention_mask,
        # Additional kwargs for sdpa
        allow_is_causal_skip=False,
        allow_is_bidirectional_skip=allow_is_bidirectional_skip,
        dtype=dtype,  # Additional kwarg for eager
        config=config,  # Pass the config as well, in case someone wants to easily have their own mask_interface
        use_vmap=use_vmap,  # Short-circuit to non-vmap expansions for the mask
        device=device,
    )
    return attention_mask

