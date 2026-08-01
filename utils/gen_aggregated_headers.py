
def gen_aggregated_headers(
    *,
    native_functions: Sequence[NativeFunction],
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
    structured_native_functions: Sequence[NativeFunctionsGroup],
    static_dispatch_idx: list[BackendIndex],
    selector: SelectiveBuilder,
    backend_indices: dict[DispatchKey, BackendIndex],
    cpu_fm: FileManager,
    device_fms: dict[str, FileManager],
    functions_keys: set[DispatchKey],
    dispatch_keys: Sequence[DispatchKey],
    rocm: bool,
) -> None:
    # Buck doesn't support dynamic output files, so we aggregate all operator
    # headers into a single file
    cpu_fm.write(
        "NativeMetaFunctions.h",
        lambda: {
            "NativeMetaFunctions_includes": [],
            "NativeMetaFunctions_declarations": list(
                mapMaybe(compute_meta_function_declaration, structured_native_functions)
            ),
        },
    )
    method_native_functions = [
        fn for fn in native_functions if Variant.method in fn.variants
    ]
    non_method_native_functions = [
        fn for fn in native_functions if fn not in method_native_functions
    ]
    cpu_fm.write(
        "MethodOperators.h",
        lambda: {
            "MethodOperators_includes": [],
            "MethodOperators_declarations": list(
                mapMaybe(
                    ComputeOperators(
                        Target.DECLARATION,
                        static_dispatch_backend_indices=static_dispatch_idx,
                    ),
                    method_native_functions,
                )
            ),
        },
    )
    cpu_fm.write(
        "Operators.h",
        lambda: {
            "Operators_includes": ["#include <ATen/MethodOperators.h>"],
            "Operators_declarations": list(
                mapMaybe(
                    ComputeOperators(
                        Target.DECLARATION,
                        static_dispatch_backend_indices=static_dispatch_idx,
                    ),
                    non_method_native_functions,
                )
            ),
        },
    )
    cpu_fm.write(
        "Functions.h",
        lambda: {
            "static_dispatch_extra_headers": static_dispatch_extra_headers(
                static_dispatch_idx
            ),
            "Functions_includes": ["#include <ATen/Operators.h>"],
            "Functions_declarations": list(
                mapMaybe(
                    ComputeFunction(),
                    native_functions,
                )
            ),
        },
    )
    declarations = get_native_function_declarations(
        grouped_native_functions=grouped_native_functions,
        backend_indices=backend_indices,
    )
    cpu_fm.write(
        "NativeFunctions.h",
        lambda: {
            "NativeFunctions_includes": ["#include <ATen/NativeMetaFunctions.h>"],
            "NativeFunctions_declarations": declarations,
        },
    )

    for dispatch_key in dispatch_keys:
        fm = file_manager_from_dispatch_key(dispatch_key, device_fms, cpu_fm)
        if dispatch_key in functions_keys:
            inl_headers = f"#include <ATen/{dispatch_key}Functions_inl.h>"

            fm.write_with_template(
                f"{dispatch_key}Functions.h",
                "DispatchKeyFunctions.h",
                lambda: {
                    "dispatch_key": str(dispatch_key),
                    "inline_headers": inl_headers,
                },
            )
            fm.write_with_template(
                f"{dispatch_key}Functions_inl.h",
                "DispatchKeyFunctions_inl.h",
                lambda: {
                    "DispatchKeyFunctions_inl_includes": [],
                    "dispatch_namespace": dispatch_key.lower(),
                    "dispatch_namespaced_declarations": get_namespaced_declaration(
                        grouped_native_functions=grouped_native_functions,
                        dispatch_key=dispatch_key,
                        backend_idx=backend_indices[dispatch_key],
                        selector=selector,
                        rocm=rocm,
                        symint=True,
                    ),
                },
            )

        del fm

