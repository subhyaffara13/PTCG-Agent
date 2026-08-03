from typing import Callable

def get_ns_grouped_kernels(
    *,
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
    backend_indices: dict[DispatchKey, BackendIndex],
    native_function_decl_gen: Callable[
        [NativeFunctionsGroup | NativeFunction, BackendIndex], list[str]
    ] = dest.compute_native_function_declaration,
) -> dict[str, list[str]]:
    ns_grouped_kernels: dict[str, list[str]] = defaultdict(list)
    for f in grouped_native_functions:
        native_function_namespaces = set()
        dispatch_keys = set()
        for dispatch_key, backend_idx in backend_indices.items():
            backend_metadata = backend_idx.get_kernel(f)
            if backend_metadata:
                namespace = backend_metadata.cpp_namespace
                dispatch_keys.add(dispatch_key)
                native_function_namespaces.add(namespace)
            else:
                namespace = DEFAULT_KERNEL_NAMESPACE
            if len(native_function_namespaces) > 1:
                raise AssertionError(
                    f"Codegen only supports one namespace per operator, "
                    f"got {native_function_namespaces} from {dispatch_keys}"
                )
            ns_grouped_kernels[namespace].extend(
                native_function_decl_gen(f, backend_idx)
            )
    return ns_grouped_kernels

