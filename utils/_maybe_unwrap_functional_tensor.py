
def _maybe_unwrap_functional_tensor(maybe_tensor: Any, *, reapply_views: bool) -> Any:
    if not isinstance(maybe_tensor, torch.Tensor):
        return maybe_tensor
    if isinstance(maybe_tensor, FunctionalTensor):
        maybe_tensor = maybe_tensor.elem

    if not torch._is_functional_tensor(maybe_tensor):
        # If it's not a functional tensor, just return it.
        # This can happen if we functionalize a fn that returns a global,
        # which was never wrapped properly.
        return maybe_tensor
    # Sync any pending updates on the output tensor
    torch._sync(maybe_tensor)
    return _unwrap_functional_tensor(maybe_tensor, reapply_views)

