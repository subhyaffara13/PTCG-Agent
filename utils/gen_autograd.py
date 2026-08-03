import os

def gen_autograd(
    native_functions_path: str,
    tags_path: str,
    out: str,
    autograd_dir: str,
    operator_selector: SelectiveBuilder,
    disable_autograd: bool = False,
) -> None:
    # Parse and load derivatives.yaml
    differentiability_infos, used_dispatch_keys = load_derivatives(
        os.path.join(autograd_dir, "derivatives.yaml"), native_functions_path, tags_path
    )

    template_path = os.path.join(autograd_dir, "templates")

    native_funcs = parse_native_yaml(native_functions_path, tags_path).native_functions
    fns = sorted(
        filter(
            operator_selector.is_native_function_selected_for_training, native_funcs
        ),
        key=lambda f: cpp.name(f.func),
    )
    fns_with_diff_infos: list[NativeFunctionWithDifferentiabilityInfo] = (
        match_differentiability_info(fns, differentiability_infos)
    )

    # Generate VariableType.h/cpp
    if not disable_autograd:
        gen_variable_type(
            out,
            native_functions_path,
            tags_path,
            fns_with_diff_infos,
            template_path,
            used_dispatch_keys,
        )

        gen_inplace_or_view_type(
            out, native_functions_path, tags_path, fns_with_diff_infos, template_path
        )

        # operator filter not applied as tracing sources are excluded in selective build
        gen_trace_type(out, native_funcs, template_path)
    # Generate Functions.h/cpp
    gen_autograd_functions_lib(out, differentiability_infos, template_path)

    # Generate variable_factories.h
    gen_variable_factories(out, native_functions_path, tags_path, template_path)

    # Generate ViewFuncs.h/cpp
    gen_view_funcs(out, fns_with_diff_infos, template_path)

