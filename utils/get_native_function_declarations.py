
def get_native_function_declarations(
    *,
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
    backend_indices: dict[DispatchKey, BackendIndex],
    native_function_decl_gen: Callable[
        [NativeFunctionsGroup | NativeFunction, BackendIndex], list[str]
    ] = dest.compute_native_function_declaration,
) -> list[str]:
    """
    Generate kernel declarations, in `NativeFunction(s).h`.
    :param grouped_native_functions: a sequence of `NativeFunction` or `NativeFunctionGroup`.
    :param backend_indices: kernel collections grouped by dispatch key.
    :param native_function_decl_gen: callable to generate kernel declaration for each `NativeFunction`.
    :return: a list of string, from the string with all declarations, grouped by namespaces, split by newline.
    """

    ns_grouped_kernels = get_ns_grouped_kernels(
        grouped_native_functions=grouped_native_functions,
        backend_indices=backend_indices,
        native_function_decl_gen=native_function_decl_gen,
    )
    return get_native_function_declarations_from_ns_grouped_kernels(
        ns_grouped_kernels=ns_grouped_kernels
    )

