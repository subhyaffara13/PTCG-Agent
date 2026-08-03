from typing import Any, Callable

def prepare_aot_module_simplified(
    mod: nn.Module,
    args: Iterable[Any],
    kwargs: dict[str, Any] | None,
    decompositions: dict[OpOverload, Callable[..., Any]] | None,
    keep_inference_input_mutations: bool,
    ignore_shape_env: bool,
    flatten: bool,
    *,
    force_non_lazy_backward_lowering: bool = False,
    disable_functionalization: bool = False,
    _record_nn_module_stack: bool = False,
    _disable_torch_fn_metadata_mode: bool = False,
) -> tuple[
    Any,
    list[torch.nn.Parameter | Tensor],
    list[str],
    list[str],
    FakifiedFlatArgs,
    list[Any],
    AOTConfig,
    FakeTensorMode,
    ShapeEnv | None,
    pytree.TreeSpec | None,
    PytreeThunk | None,
    list[int],
]:
    if not flatten:
        if kwargs is not None:
            raise AssertionError("kwargs must be None when flatten=False")
    elif kwargs is None:
        kwargs = {}

    (
        params_buffers_flat,
        params_spec,
        buffers_spec,
        full_args,
        full_args_descs,
        aot_config,
    ) = prepare_aot_config(
        mod,
        args,
        decompositions,
        keep_inference_input_mutations,
        ignore_shape_env,
        force_non_lazy_backward_lowering=force_non_lazy_backward_lowering,
        disable_functionalization=disable_functionalization,
        _disable_torch_fn_metadata_mode=_disable_torch_fn_metadata_mode,
    )

    params_buffers_spec = params_spec + buffers_spec

    # NB: This doesn't change the in/out convention, except adding the
    # parameters as explicit arguments
    functional_call = create_functional_call(
        mod,
        params_buffers_spec,
        aot_config.num_params_buffers,
        strict_out_tuple=not flatten,
        # We need this for export to run ModuleStackTracer
        # instead of PythonKeyTracer
        store_orig_mod=_record_nn_module_stack,
    )

    in_spec, out_spec = None, None
    if flatten:
        functional_call, out_spec = create_tree_flattened_fn(
            functional_call, full_args, kwargs
        )
        full_args, in_spec = pytree.tree_flatten((full_args, kwargs))

    # TODO: it would be better to put pytree information in here
    full_args_descs.extend(
        PlainAOTInput(i) for i in range(len(full_args) - len(full_args_descs))
    )

    fake_mode, shape_env = construct_fake_mode(full_args, aot_config)
    # NB: full_args_descs not needed here, fake_flat_args is 1:1 with full_args
    fake_flat_args, act_input_indices = process_inputs(
        full_args, aot_config, fake_mode, shape_env, ignore_shape_env
    )

    return (
        functional_call,
        params_buffers_flat,
        params_spec,
        buffers_spec,
        fake_flat_args,
        full_args_descs,
        aot_config,
        fake_mode,
        shape_env,
        in_spec,
        out_spec,
        act_input_indices,
    )

