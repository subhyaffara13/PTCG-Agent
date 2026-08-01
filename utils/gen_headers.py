
def gen_headers(
    *,
    native_functions: Sequence[NativeFunction],
    valid_tags: set[str],
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
    structured_native_functions: Sequence[NativeFunctionsGroup],
    static_dispatch_idx: list[BackendIndex],
    selector: SelectiveBuilder,
    backend_indices: dict[DispatchKey, BackendIndex],
    headeronly_fm: FileManager,
    core_fm: FileManager,
    cpu_fm: FileManager,
    device_fms: dict[str, FileManager],
    ops_fm: FileManager,
    dispatch_keys: Sequence[DispatchKey],
    functions_keys: set[DispatchKey],
    rocm: bool,
    per_operator_headers: bool,
) -> None:
    if per_operator_headers:
        gen_per_operator_headers(
            native_functions=native_functions,
            grouped_native_functions=grouped_native_functions,
            static_dispatch_idx=static_dispatch_idx,
            selector=selector,
            backend_indices=backend_indices,
            cpu_fm=cpu_fm,
            device_fms=device_fms,
            ops_fm=ops_fm,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=rocm,
        )
    else:
        gen_aggregated_headers(
            native_functions=native_functions,
            grouped_native_functions=grouped_native_functions,
            structured_native_functions=structured_native_functions,
            static_dispatch_idx=static_dispatch_idx,
            selector=selector,
            backend_indices=backend_indices,
            cpu_fm=cpu_fm,
            device_fms=device_fms,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=rocm,
        )

    core_fm.write(
        "TensorBody.h",
        lambda: {
            "tensor_method_declarations": list(
                mapMaybe(
                    ComputeTensorMethod(
                        target=Target.DECLARATION,
                        static_dispatch_backend_indices=static_dispatch_idx,
                    ),
                    native_functions,
                )
            ),
            "tensor_method_definitions": list(
                mapMaybe(
                    ComputeTensorMethod(
                        target=Target.DEFINITION,
                        static_dispatch_backend_indices=static_dispatch_idx,
                    ),
                    native_functions,
                )
            ),
        },
    )

    cpu_fm.write(
        "RedispatchFunctions.h",
        lambda: {
            "function_redispatch_definitions": list(
                mapMaybe(ComputeRedispatchFunction(), native_functions)
            ),
        },
    )

    cpu_fm.write(
        "RegistrationDeclarations.h",
        lambda: {
            "registration_declarations": [
                compute_registration_declarations(f, backend_indices)
                for f in native_functions
            ],
        },
    )

    cpu_fm.write(
        "VmapGeneratedPlumbing.h", lambda: gen_all_vmap_plumbing(native_functions)
    )

    def gen_aten_interned_strings() -> dict[str, str]:
        attrs: set[str] = set()  # All function argument names
        names = set()  # All ATen function names
        for func in native_functions:
            names.add(str(func.func.name.name))
            # Some operators don't have a functional variant but we still create a
            # symbol without the underscore
            names.add(func.func.name.name.base)

            attrs.update(arg.name for arg in func.func.schema_order_arguments())

        # These are keywords in C++, so aren't valid symbol names
        # https://en.cppreference.com/w/cpp/language/operator_alternative
        names -= {
            "and",
            "and_eq",
            "bitand",
            "bitor",
            "compl",
            "not",
            "not_eq",
            "or",
            "or_eq",
            "xor",
            "xor_eq",
        }

        return {
            "aten_symbols": " \\\n".join(
                [f"_(aten, {name})" for name in sorted(names)]
            ),
            "attr_symbols": " \\\n".join(
                [f"_(attr, {name})" for name in sorted(attrs)]
            ),
        }

    core_fm.write("aten_interned_strings.h", gen_aten_interned_strings)

    def gen_tags_enum() -> dict[str, str]:
        return {"enum_of_valid_tags": (",\n".join(sorted(valid_tags)))}

    headeronly_fm.write("enum_tag.h", gen_tags_enum)

