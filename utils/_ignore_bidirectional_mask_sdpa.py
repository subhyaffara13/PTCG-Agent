
def _ignore_bidirectional_mask_sdpa(
    padding_mask: torch.Tensor | None,
    kv_length: int,
    local_attention_size: int | None = None,
) -> bool:
    """
    Detects whether the bidirectional mask can be ignored in case PyTorch's SDPA is used.

    In case no token is masked in the 2D `padding_mask` argument and no local attention constraint applies
    (i.e. `local_attention_size` is None or `kv_length < local_attention_size`), we skip mask creation,
    allowing to dispatch to the flash attention kernel (that can otherwise not be used if a custom `attn_mask` is
    passed).
    """
    if _is_torch_xpu_available:
        # XPU devices have special handling for mask skipping:
        # - Skip if no padding and no local attention constraint
        return _can_skip_bidirectional_mask_xpu(padding_mask, kv_length, local_attention_size)

    # When using `torch.export` or `torch.onnx.dynamo_export`, we need to avoid to check the contents of the mask;
    # otherwise, we will encounter dynamic control flows
    if (
        not is_tracing(padding_mask)
        and (padding_mask is None or padding_mask.all())
        # in this case we need to add special patterns to the mask so cannot be skipped otherwise
        and (local_attention_size is None or kv_length < local_attention_size)
    ):
        return True

    return False

