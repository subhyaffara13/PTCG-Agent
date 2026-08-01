
def get_kernel_namespace(
    *, f: NativeFunction | NativeFunctionsGroup, backend_idx: BackendIndex
) -> str:
    backend_metadata = backend_idx.get_kernel(f)
    if backend_metadata and "::native" not in backend_metadata.cpp_namespace:
        func_name = (
            f.func.name if isinstance(f, NativeFunction) else f.functional.func.name
        )
        raise AssertionError(
            f"The kernel for function {func_name} "
            f"with dispatch key {backend_idx.dispatch_key} "
            f"has a namespace {backend_metadata.cpp_namespace} and it's not ending with '::native'."
        )
    return (
        backend_metadata.cpp_namespace if backend_metadata else DEFAULT_KERNEL_NAMESPACE
    )

