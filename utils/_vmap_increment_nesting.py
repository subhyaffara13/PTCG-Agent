
def _vmap_increment_nesting(batch_size: int, randomness: str) -> int:
    """
    Thin wrapper around torch._C._vmap_increment_nesting that is used
    to proxy in export/compile graph
    """
    from torch._export.utils import _maybe_find_pre_dispatch_tf_mode_for_export

    mode = _maybe_find_pre_dispatch_tf_mode_for_export()

    if mode:
        return torch.overrides.handle_torch_function(
            _vmap_increment_nesting, (batch_size,), batch_size, randomness
        )
    res = _vmap_increment_nesting_impl(batch_size, randomness)
    return res

