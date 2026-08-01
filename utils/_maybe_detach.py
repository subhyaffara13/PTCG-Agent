
def _maybe_detach(x, any_ret_has_alias_info):
    # We detach for two separate reasons:
    # - For view ops, we need to ensure that when the tensor is returned from
    #   CachedDispatchMode, as_view sees that the AutogradMeta is nullptr
    # - Avoid reference cycles
    # For case 1, it is not enough to check whether x has differentiable dtype
    # because non-differentiable dtype can have non-nullptr AutogradMeta, e.g.
    # when the tensor is a view.
    if isinstance(x, torch.Tensor) and (x.is_floating_point() or x.is_complex() or any_ret_has_alias_info):
        with torch._C._SetExcludeDispatchKeyGuard(torch._C.DispatchKey.ADInplaceOrView, False):
            # Ensure that view performed beneath autograd properly propagates
            # version counter. TODO: Use reentrant_dispatch instead of
            # manually manipulating dispatch keys. Using reentrant_dispatch
            # would respect inference_mode, though that is not relevant for
            # this case.
            x = x.detach()
    return x

