
def _remove_batch_dim(
    self: torch.Tensor, level: int, batch_size: int, out_dim: int
) -> torch.Tensor:
    """
    Thin wrapper around torch._C._remove_batch_dim that is used to proxy in
    PT2 export/compile fx graph
    """
    from torch._export.utils import _maybe_find_pre_dispatch_tf_mode_for_export

    mode = _maybe_find_pre_dispatch_tf_mode_for_export()

    if mode:
        return torch.overrides.handle_torch_function(
            _remove_batch_dim, (self,), self, level, batch_size, out_dim
        )

    res = _remove_batch_dim_impl(self, level, batch_size, out_dim)
    return res

