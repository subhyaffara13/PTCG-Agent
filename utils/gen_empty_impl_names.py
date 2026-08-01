
def gen_empty_impl_names(
    backend_index: BackendIndex,
) -> tuple[str | None, str | None]:
    empty_impl = None
    empty_strided_impl = None

    if backend_index.dispatch_key in (
        DispatchKey.Meta,
        DispatchKey.CPU,
        DispatchKey.CUDA,
        DispatchKey.MPS,
        DispatchKey.XPU,
        DispatchKey.MTIA,
    ):
        dispatch = str(backend_index.dispatch_key).lower()
        empty_impl = f"at::detail::empty_{dispatch}"
        empty_strided_impl = f"at::detail::empty_strided_{dispatch}"
    elif backend_index.dispatch_key in (
        DispatchKey.CompositeExplicitAutogradNonFunctional,
        DispatchKey.QuantizedCPU,
        DispatchKey.QuantizedCUDA,
        DispatchKey.XPU,
    ):
        empty_impl = "at::empty"
        empty_strided_impl = "at::empty_strided"

    return empty_impl, empty_strided_impl

