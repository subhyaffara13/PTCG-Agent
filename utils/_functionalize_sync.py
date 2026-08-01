
def _functionalize_sync(t):
    # This code lives in python instead of C++ since conditioning on a certain python subclass
    # is much more of a pain in C++.
    from torch._subclasses.functional_tensor import FunctionalTensor

    if isinstance(t, FunctionalTensor):
        # If a FunctionalTensorMode is active while syncing, we don't want it to intercept any ops that get called
        # when we sync our inner tensor.
        # Why?
        # (1) If there are input mutations in the graph, then they will be re-applied during
        #     AOTAutograd when we call _sync() from inside of our functionalization kernels.
        # (2) _sync() causes us to regenerate our updated the tensor from the updated base,
        #     which dispatches to a bunch of view ops
        # (3) The input to these view ops is our inner FunctionalTensorWrapper
        #     (since the sync was called from C++), not the python FunctionalTensor
        # (4) if a python FunctionalTensorMode is active, it will complain when it intercepts
        #     the view op, since it will see an input that is a C++ FunctionalTensorWrapper
        #     (aka a normal torch.Tensor) instead of a python `FunctionalTensor).
        maybe_functional_mode = torch._C._unset_dispatch_mode(
            torch._C._TorchDispatchModeKey.FUNCTIONAL
        )
        try:
            torch._functionalize_sync(t.elem)  # type: ignore[attr-defined]
        finally:
            if maybe_functional_mode is not None:
                torch._C._set_dispatch_mode(maybe_functional_mode)
    else:
        torch._functionalize_sync(t)  # type: ignore[attr-defined]

