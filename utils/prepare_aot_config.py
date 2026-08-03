from typing import Any, Callable

def prepare_aot_config(
    mod: nn.Module,
    args: Iterable[Any],
    decompositions: dict[OpOverload, Callable[..., Any]] | None,
    keep_inference_input_mutations: bool,
    ignore_shape_env: bool,
    *,
    force_non_lazy_backward_lowering: bool = False,
    disable_functionalization: bool = False,
    _disable_torch_fn_metadata_mode: bool = False,
) -> tuple[
    list[torch.nn.Parameter | Tensor],
    list[str],
    list[str],
    list[Any],
    list[Any],
    AOTConfig,
]:
    # TODO: There's something a bit suspicious here; typically simplified
    # module shouldn't actually have any parameters...
    params = dict(mod.named_parameters(remove_duplicate=False))
    buffers = dict(dict(mod.named_buffers(remove_duplicate=False)))

    params_flat, params_spec = list(params.values()), list(params.keys())
    params_len = len(params_flat)

    buffers_flat, buffers_spec = list(buffers.values()), list(buffers.keys())
    buffers_len = len(buffers_flat)

    params_buffers = {**params, **buffers}
    params_buffers_flat = params_flat + buffers_flat

    full_args = [*params_flat, *buffers_flat, *args]

    # OK, set up the descs

    full_args_descs: list[DifferentiableAOTInput] = []
    full_args_descs.extend(ParamAOTInput(fqn) for fqn in params_spec)
    full_args_descs.extend(BufferAOTInput(fqn) for fqn in buffers_spec)

    # TODO: These tracing_context fields should become unnecessary once we
    # always maintain sources on all arguments
    if tracing_context := torch._guards.TracingContext.try_get():
        # NB: TracingContext misnames this, the "params" here also contains
        # buffers
        tracing_context.params_flat = params_buffers_flat
        (
            tracing_context.params_flat_unwrap_subclasses,
            tracing_context.params_unwrapped_to_flat_index,
        ) = unwrap_tensor_subclasses_with_indices_to_original(params_buffers_flat)

    # TODO: Might be nice to hold on to the Dynamo source here in full_args_descs!
    (
        aot_autograd_arg_pos_to_source,
        static_input_indices,
    ) = _try_get_metadata_from_dynamo(
        mod, params_buffers.keys(), len(full_args), full_args_descs
    )

    dynamic_shapes = False
    for x in full_args:
        if isinstance(x, FakeTensor):
            dynamic_shapes = x.fake_mode.shape_env is not None
            break

    aot_config = AOTConfig(
        fw_compiler=None,
        bw_compiler=None,
        inference_compiler=None,
        partition_fn=None,
        decompositions=decompositions,
        num_params_buffers=params_len + buffers_len,
        aot_id=next(AOT_COUNTER),
        keep_inference_input_mutations=keep_inference_input_mutations,
        dynamic_shapes=dynamic_shapes,
        # pyrefly: ignore[bad-argument-type]
        aot_autograd_arg_pos_to_source=aot_autograd_arg_pos_to_source,
        static_input_indices=static_input_indices,
        is_export=False,
        no_tangents=False,
        cache_info=None,
        ignore_shape_env=ignore_shape_env,
        precompile_backend_id=getattr(mod, "_backend_id", None),
        force_non_lazy_backward_lowering=force_non_lazy_backward_lowering,
        disable_functionalization=disable_functionalization,
        _disable_torch_fn_metadata_mode=_disable_torch_fn_metadata_mode,
    )

    return (
        params_buffers_flat,
        params_spec,
        buffers_spec,
        full_args,
        full_args_descs,
        aot_config,
    )

