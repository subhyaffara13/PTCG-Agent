
def get_static_dispatch_backend(
    f: NativeFunction, backend_index: BackendIndex
) -> DispatchKey | None:
    if f.structured_delegate is not None or backend_index.has_kernel(f):
        # TODO: for ops with structured_delegate it should check the dispatch table of
        # the out variant instead. For now, these structured ops all have CPU/CUDA kernels
        # so we always dispatch to the `backend`, but this could be wrong when we
        # migrate math/default_backend ops to use structured delegate.
        return backend_index.dispatch_key
    elif f.has_composite_explicit_autograd_kernel:
        return DispatchKey.CompositeExplicitAutograd
    elif f.has_composite_explicit_autograd_non_functional_kernel:
        return DispatchKey.CompositeExplicitAutogradNonFunctional
    elif f.has_composite_implicit_autograd_kernel:
        return DispatchKey.CompositeImplicitAutograd
    elif f.has_composite_implicit_autograd_nested_tensor_kernel:
        return DispatchKey.CompositeImplicitAutogradNestedTensor
    return None

