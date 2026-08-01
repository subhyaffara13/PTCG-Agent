
def _flex_attention_autocast_impl(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    score_mod: Callable,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple,
    mask_mod_other_buffers: tuple,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Forward-only autocast shim: cast Q/K/V to the active autocast dtype, then
    redispatch with Autocast keys excluded so we hit the normal implementation.
    """
    device_type = query.device.type
    autocast_dtype = torch.get_autocast_dtype(device_type)

    query = _autocast_cast(query, device_type, autocast_dtype)
    key = _autocast_cast(key, device_type, autocast_dtype)
    value = _autocast_cast(value, device_type, autocast_dtype)

    autocast_keyset = torch._C.DispatchKeySet(
        DispatchKey.AutocastCPU
    ) | torch._C.DispatchKeySet(DispatchKey.AutocastCUDA)
    with torch._C._ExcludeDispatchKeyGuard(autocast_keyset):
        return flex_attention(
            query,
            key,
            value,
            score_mod,
            block_mask,
            scale,
            kernel_options,
            score_mod_other_buffers,
            mask_mod_other_buffers,
        )

