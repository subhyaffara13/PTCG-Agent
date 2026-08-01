
def clone_preserve_strides(x: torch.Tensor) -> torch.Tensor:
    if 0 in x.size():
        # Short-circuits if the shape has no elements
        needed_size = 0
    else:
        needed_size = (
            sum((shape - 1) * stride for shape, stride in zip(x.size(), x.stride())) + 1
        )
    buffer = torch.as_strided(x, (needed_size,), (1,)).clone()
    return torch.as_strided(buffer, x.size(), x.stride())


def clone_preserve_strides(x):
    needed_size = compute_required_storage_length(
        x.size(), x.stride(), x.storage_offset()
    )
    # Our eager implementations for *_scatter ops are all primitives w.r.t autograd,
    # so these as_strided() calls are not seen by autograd.
    # We need to mimic this behavior in our ref/prim implementations.
    # TODO: a better way to handle this would be with a new op, "_unsafe_as_strided"
    # We should revisit this when we add a compositional as_strided op,
    # and also as part of https://github.com/pytorch/pytorch/issues/90507
    try:
        old = torch._C._dispatch_tls_is_dispatch_key_excluded(
            torch._C.DispatchKey.ADInplaceOrView
        )
        torch._C._dispatch_tls_set_dispatch_key_excluded(
            torch._C.DispatchKey.ADInplaceOrView, True
        )
        buffer = torch.as_strided(x, (needed_size,), (1,), 0).clone()
        return torch.as_strided(buffer, x.size(), x.stride(), x.storage_offset())
    finally:
        torch._C._dispatch_tls_set_dispatch_key_excluded(
            torch._C.DispatchKey.ADInplaceOrView, old
        )

