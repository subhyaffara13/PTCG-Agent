
def gen_variable_type(
    out: str,
    native_yaml_path: str,
    tags_yaml_path: str,
    fns_with_diff_infos: list[NativeFunctionWithDifferentiabilityInfo],
    template_path: str,
    used_keys: set[str],
) -> None:
    """VariableType.h and VariableType.cpp body

    This is the at::Type subclass for differentiable tensors. The
    implementation of each function dispatches to the base tensor type to
    compute the output. The grad_fn is attached to differentiable functions.
    """
    fm = FileManager(install_dir=out, template_dir=template_path, dry_run=False)
    fm.write(
        "VariableType.h",
        lambda: {
            "generated_comment": "@"
            + f"generated from {fm.template_dir_for_comments()}/VariableType.h"
        },
    )

    # helper that generates a TORCH_LIBRARY_IMPL macro for each
    # dispatch key that appears in derivatives.yaml
    def wrapper_registrations(used_keys: set[str]) -> str:
        library_impl_macro_list: list[str] = []
        for key in sorted(used_keys):
            dispatch_key = key
            if key == "Default":
                dispatch_key = "Autograd"
            library_impl_macro = (
                f"TORCH_LIBRARY_IMPL(aten, {dispatch_key}, m) "
                + "{\n"
                + "${"
                + f"wrapper_registrations_{key}"
                + "}\n}"
            )
            library_impl_macro_list += [library_impl_macro]
        return "\n\n".join(library_impl_macro_list)

    # Generate a new template from VariableType.cpp which replaces ${wrapper_registrations}
    # with per key TORCH_LIBRARY_IMPL macros for each key that appears in derivatives.yaml
    fm1 = FileManager(
        install_dir=out + "/templates", template_dir=template_path, dry_run=False
    )
    fm1.write(
        "VariableType.cpp",
        lambda: {
            "type_derived_method_definitions": "\n\n".join(
                [
                    "${" + f"type_derived_method_definitions_{key}" + "}"
                    for key in sorted(used_keys)
                ]
            ),
            "wrapper_registrations": wrapper_registrations(used_keys),
        },
    )

    # Generate final VariableType_*.cpp files from the generated template
    fm2 = FileManager(install_dir=out, template_dir=out + "/templates", dry_run=False)

    sharded_keys = set(
        [f"type_derived_method_definitions_{key}" for key in sorted(used_keys)]
        + [f"wrapper_registrations_{key}" for key in sorted(used_keys)]
    )
    # NOTE: see Note [Sharded File] at the top of the VariableType.cpp
    # template regarding sharding of the generated files.
    fm2.write_sharded(
        "VariableType.cpp",
        [fn for fn in fns_with_diff_infos if use_derived(fn)],
        key_fn=lambda fn: cpp.name(fn.func.func),
        base_env={
            "generated_comment": "@"
            + f"generated from {fm.template_dir_for_comments()}/VariableType.cpp",
        },
        env_callable=gen_variable_type_func,
        num_shards=5,
        sharded_keys=sharded_keys,
    )

