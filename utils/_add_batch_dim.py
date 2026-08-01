
def _add_batch_dim(self: torch.Tensor, batch_dim: int, level: int) -> torch.Tensor:
    """
    Thin wrapper around torch._C._add_batch_dim that is used to proxy in
    PT2 export/compile fx graph
    """
    from torch._export.utils import _maybe_find_pre_dispatch_tf_mode_for_export

    mode = _maybe_find_pre_dispatch_tf_mode_for_export()
    batch_dim = self.ndim + batch_dim if batch_dim < 0 else batch_dim

    if mode:
        return torch.overrides.handle_torch_function(
            _add_batch_dim, (self,), self, batch_dim, level
        )

    res = _add_batch_dim_impl(self, batch_dim, level)
    return res

