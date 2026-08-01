
def _prepare_4d_causal_attention_mask_for_sdpa(
    attention_mask: torch.Tensor | None,
    input_shape: torch.Size | tuple | list,
    inputs_embeds: torch.Tensor,
    past_key_values_length: int,
    sliding_window: int | None = None,
):
    """
    Prepares the correct `attn_mask` argument to be used by `torch.nn.functional.scaled_dot_product_attention`.

    In case no token is masked in the `attention_mask` argument, we simply set it to `None` for the cases `query_length == 1` and
    `key_value_length == query_length`, and rely instead on SDPA `is_causal` argument to use causal/non-causal masks,
    allowing to dispatch to the flash attention kernel (that can otherwise not be used if a custom `attn_mask` is passed).
    """
    attn_mask_converter = AttentionMaskConverter(is_causal=True, sliding_window=sliding_window)

    key_value_length = input_shape[-1] + past_key_values_length

    # torch.jit.trace, symbolic_trace and torchdynamo with fullgraph=True are unable to capture the controlflow `is_causal=attention_mask is None and q_len > 1`
    # used as an SDPA argument. We keep compatibility with these tracing tools by always using SDPA's `attn_mask` argument in case we are tracing.
    # TODO: For dynamo, rather use a check on fullgraph=True once this is possible (https://github.com/pytorch/pytorch/pull/120400).
    is_tracing_ = is_tracing(inputs_embeds)

    ignore_causal_mask = AttentionMaskConverter._ignore_causal_mask_sdpa(
        attention_mask=attention_mask,
        inputs_embeds=inputs_embeds,
        past_key_values_length=past_key_values_length,
        sliding_window=sliding_window,
    )

    if ignore_causal_mask:
        expanded_4d_mask = None
    elif attention_mask is None:
        expanded_4d_mask = attn_mask_converter.to_causal_4d(
            input_shape[0], input_shape[-1], key_value_length, dtype=inputs_embeds.dtype, device=inputs_embeds.device
        )
    else:
        if attention_mask.dim() == 4:
            expanded_4d_mask = attention_mask
        else:
            expanded_4d_mask = attn_mask_converter.to_4d(
                attention_mask,
                input_shape[-1],
                dtype=inputs_embeds.dtype,
                key_value_length=key_value_length,
            )

        # Attend to all tokens in masked rows from the causal_mask, for example the relevant first rows when
        # using left padding. This is required by F.scaled_dot_product_attention memory-efficient attention path.
        # Details: https://github.com/pytorch/pytorch/issues/110213
        if not is_tracing_ and expanded_4d_mask.device.type in ["cuda", "xpu"]:
            expanded_4d_mask = AttentionMaskConverter._unmask_unattended(
                expanded_4d_mask, min_dtype=torch.finfo(inputs_embeds.dtype).min
            )

    return expanded_4d_mask

