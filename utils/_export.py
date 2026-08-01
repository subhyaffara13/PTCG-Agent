
def _export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: dict[str, Any] | None = None,
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any] | None = None,
    *,
    strict: bool = True,
    preserve_module_call_signature: tuple[str, ...] = (),
    pre_dispatch: bool = False,
    prefer_deferred_runtime_asserts_over_guards: bool = False,
) -> ExportedProgram:
    """
    Traces either an nn.Module's forward function or just a callable with PyTorch
    operations inside and produce a ExportedProgram.

    Args:
        mod: the `nn.Module` to trace.

        args: example positional inputs.

        kwargs: optional example keyword inputs.

        dynamic_shapes:
         An optional argument where the type should either be:
         1) a dict from argument names of ``f`` to their dynamic shape specifications,
         2) a tuple that specifies dynamic shape specifications for each input in original order.
         If you are specifying dynamism on keyword args, you will need to pass them in the order that
         is defined in the original function signature.

         The dynamic shape of a tensor argument can be specified as either
         (1) a dict from dynamic dimension indices to :func:`Dim` types, where it is
         not required to include static dimension indices in this dict, but when they are,
         they should be mapped to None; or (2) a tuple / list of :func:`Dim` types or None,
         where the :func:`Dim` types correspond to dynamic dimensions, and static dimensions
         are denoted by None. Arguments that are dicts or tuples / lists of tensors are
         recursively specified by using mappings or sequences of contained specifications.

        preserve_module_call_signature: A list of submodule paths for which the original
            calling conventions are preserved as metadata.

        prefer_deferred_runtime_asserts_over_guards:
         With the current dynamic shapes language for dims and derived dims, we can run into constraints
         that are not expressible with the language. For example, flattening a matrix and adding to a vector,
         both fully dynamic (i.e. x.reshape([-1]) + y) emits a guard s0 * s1 = s2, which is not expressible.
         By default, we either raise a constraint violation error or specialize to static values.
         If this flag is set to True, we avoid erroring out and instead allow complex constraints to exist as runtime
         assertions in the graph. The sympy interpreter (torch/utils/_sympy/interp.py) will produce the math ops
         required to compute and assert the value of the guard (e.g. sym_size_int, eq, _assert_scalar).
         Additionally, if TORCH_DYNAMO_DO_NOT_EMIT_RUNTIME_ASSERTS=1 is specified, we will allow complex constraints
         while not emitting runtime asserts, returning a cleaner graph with lesser guarantees around dynamic shapes.

    Returns:
        An ExportedProgram containing the traced module.
    """

    from torch._utils_internal import export_training_ir_rollout_check

    global _EXPORT_FLAGS, _EXPORT_MODULE_HIERARCHY
    _EXPORT_MODULE_HIERARCHY = _get_module_hierarchy(mod)

    flags = set()
    flags.add("strict" if strict else "non_strict")
    flags.add("pre_dispatch" if pre_dispatch else "aot_dispatch")
    _EXPORT_FLAGS = flags

    log_export_usage(event="export.enter", flags=_EXPORT_FLAGS)

    dtrace_structured("export", payload_fn=lambda: "start!")

    # NOTE Export training IR rollout
    # Old export calls export._trace(pre_dispatch=True)
    # and there are still lot of internal/OSS callsites that
    # use export._trace(pre_dispatch=True) directly. Therefore,
    # it makes more sense to do the switch here.
    # export_training_ir_rollout_check returns True in OSS
    # while internally it returns False UNLESS otherwise specified.
    if pre_dispatch and export_training_ir_rollout_check():
        ep = _export_for_training(
            mod,
            args,
            kwargs,
            dynamic_shapes,
            strict=strict,
            preserve_module_call_signature=preserve_module_call_signature,
            prefer_deferred_runtime_asserts_over_guards=prefer_deferred_runtime_asserts_over_guards,
        )
        dtrace_structured("exported_program", payload_fn=lambda: str(ep))
        return ep

    (
        args,
        kwargs,
        original_in_spec,
        dynamic_shapes,
        verify_additional_inputs,
    ) = _process_export_inputs(mod, args, kwargs, dynamic_shapes)

    original_state_dict = _get_original_state_dict(mod)

    # Call the appropriate export function based on the strictness of tracing.
    export_func = _strict_export if strict else _non_strict_export

    export_artifact = export_func(  # type: ignore[operator]
        mod=mod,
        args=args,
        kwargs=kwargs,
        dynamic_shapes=dynamic_shapes,
        preserve_module_call_signature=preserve_module_call_signature,
        orig_in_spec=original_in_spec,
        prefer_deferred_runtime_asserts_over_guards=prefer_deferred_runtime_asserts_over_guards,
        _to_aten_func=functools.partial(
            _export_to_aten_ir,
            pre_dispatch=pre_dispatch,
        ),
    )
    export_graph_signature: ExportGraphSignature = export_artifact.aten.sig

    forward_arg_names = _get_forward_arg_names(mod, args, kwargs)
    inline_constraints = _get_inline_constraints(export_artifact.fake_mode)
    # The unbacked symint symbols are updated in aot_export
    # so we serialize them here instead of inside dynamo.
    # Note: this step must be before _get_range_constraints.
    export_artifact.aten.gm.meta["inline_constraints"] = inline_constraints
    range_constraints = _get_range_constraints(
        mod,
        export_artifact,
        args,
        kwargs,
        dynamic_shapes,
    )
    gm, module_call_graph = _get_module_call_graph(
        export_artifact,
        preserve_module_call_signature,
        strict,
        forward_arg_names,
    )

    _verify_nn_module_stack(gm)
    _verify_stack_trace(gm)
    _verify_placeholder_names(gm, export_graph_signature)

    # Remove Proxy because they cannot be deepcopied or pickled.
    torch._export.utils.remove_proxy_from_state_dict(original_state_dict, in_place=True)

    from torch._export.verifier import Verifier

    _update_gm_meta_if_possible(gm, mod)

    exported_program = ExportedProgram(
        root=gm,
        graph=gm.graph,
        graph_signature=export_graph_signature,
        state_dict=original_state_dict,
        range_constraints=range_constraints,
        module_call_graph=module_call_graph,
        example_inputs=(args, kwargs),
        constants=export_artifact.aten.constants,
        verifiers=[Verifier],
    )

    dtrace_structured("exported_program", payload_fn=lambda: str(exported_program))

    verify_additional_inputs(exported_program)
    return exported_program


def _export(name: str):
    """Exports the function in the current global namespace."""

    def wrapper(func):
        globals()[name] = func
        __all__.append(name)
        return func

    return wrapper


def _export(
    model,
    args,
    f,
    export_params=True,
    verbose=False,
    training=_C_onnx.TrainingMode.EVAL,
    input_names=None,
    output_names=None,
    operator_export_type=_C_onnx.OperatorExportTypes.ONNX,
    export_type=None,
    opset_version=None,
    do_constant_folding=True,
    dynamic_axes=None,
    keep_initializers_as_inputs=None,
    fixed_batch_size=False,
    custom_opsets=None,
    add_node_names=True,
    onnx_shape_inference=True,
    export_modules_as_functions: Any = False,
    autograd_inlining=True,
):
    if GLOBALS.in_onnx_export is not False:
        raise AssertionError("GLOBALS.in_onnx_export must be False")

    _trigger_symbolic_function_registration()

    if isinstance(model, torch.nn.DataParallel):
        raise ValueError(
            "torch.nn.DataParallel is not supported by ONNX "
            "exporter, please use 'attribute' module to "
            "unwrap model from torch.nn.DataParallel. Try "
            "torch.onnx.export(model.module, ...)"
        )

    GLOBALS.onnx_shape_inference = onnx_shape_inference

    if opset_version is None:
        opset_version = _constants.ONNX_DEFAULT_OPSET

    if opset_version > _constants.ONNX_TORCHSCRIPT_EXPORTER_MAX_OPSET:
        warnings.warn(
            f"Exporting to ONNX opset version {opset_version} is not supported. "
            f"by 'torch.onnx.export()'. "
            f"The highest opset version supported is {_constants.ONNX_TORCHSCRIPT_EXPORTER_MAX_OPSET}. "
            f"To use a newer opset version, consider 'torch.onnx.export(..., dynamo=True)'. ",
            stacklevel=2,
            category=errors.OnnxExporterWarning,
        )

    if export_modules_as_functions and opset_version < 15:
        raise ValueError(
            "`export_modules_as_functions` is not supported for `opset_version` < 15."
            "This is because `opset_version` < 15 implies IR version < 8, which means "
            "no local function support. "
        )
    if not operator_export_type:
        operator_export_type = _C_onnx.OperatorExportTypes.ONNX

    # By default, training=TrainingMode.EVAL,
    # which is good because running a model in training mode could result in
    # internal buffers getting updated, dropout getting applied, etc.
    # If you really know what you're doing, you can turn
    # training=TrainingMode.TRAINING or training=TrainingMode.PRESERVE,
    # (to preserve whatever the original training mode was.)
    GLOBALS.export_onnx_opset_version = opset_version
    GLOBALS.operator_export_type = operator_export_type

    try:
        GLOBALS.in_onnx_export = True
        _autograd_inlining_previous = GLOBALS.autograd_inlining
        GLOBALS.autograd_inlining = autograd_inlining

        module_typenames_to_export_as_functions: set[str] = set()
        if isinstance(model, (torch.nn.Module, torch.jit.ScriptModule)):
            module_typenames_to_export_as_functions = _setup_trace_module_map(
                model, export_modules_as_functions
            )

        with exporter_context(model, training, verbose):
            val_keep_init_as_ip = _decide_keep_init_as_input(
                keep_initializers_as_inputs,
                operator_export_type,
                opset_version,
            )
            val_add_node_names = _decide_add_node_names(
                add_node_names, operator_export_type
            )
            val_do_constant_folding = _decide_constant_folding(
                do_constant_folding, operator_export_type, training
            )
            # Normally f can be a file-like object, but for large models, the external data format requires a
            # valid `model_file_location`. Code in export.cpp will enforce this.
            if isinstance(f, str):
                model_file_location = f
            else:
                model_file_location = ""
            args = _decide_input_format(model, args)
            if dynamic_axes is None:
                dynamic_axes = {}
            _validate_dynamic_axes(dynamic_axes, model, input_names, output_names)

            graph, params_dict, torch_out = _model_to_graph(
                model,
                args,
                verbose,
                input_names,
                output_names,
                operator_export_type,
                val_do_constant_folding,
                fixed_batch_size=fixed_batch_size,
                training=training,
                dynamic_axes=dynamic_axes,
            )

            if custom_opsets is None:
                custom_opsets = {}

            _C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)
            node_attr_to_name = {}  # type: ignore[var-annotated]
            if module_typenames_to_export_as_functions:
                # NOTE: cannot call DCE after this pass. DCE will remove function definition nodes.
                node_attr_to_name = _C._jit_pass_onnx_function_extraction(
                    graph,
                    module_typenames_to_export_as_functions,
                    list(params_dict.keys()),
                )

            if keep_initializers_as_inputs is not True:
                params_dict = _C._jit_pass_onnx_deduplicate_initializers(  # type: ignore[assignment]
                    graph,
                    params_dict,  # type: ignore[arg-type]
                    getattr(model, "training", False),  # type: ignore[arg-type]
                )
            _C._jit_pass_onnx_assign_scoped_names_for_node_and_value(graph)
            defer_weight_export = False
            if export_params:
                (
                    proto,
                    export_map,
                    _val_use_external_data_format,
                    _node_names,
                ) = graph._export_onnx(  # type: ignore[attr-defined]
                    params_dict,
                    opset_version,
                    dynamic_axes,
                    defer_weight_export,
                    operator_export_type,
                    not verbose,
                    val_keep_init_as_ip,
                    custom_opsets,
                    val_add_node_names,
                    model_file_location,
                    node_attr_to_name,
                )
            else:
                (
                    proto,
                    export_map,
                    _,
                    _,
                ) = graph._export_onnx(  # type: ignore[attr-defined]
                    {},
                    opset_version,
                    dynamic_axes,
                    defer_weight_export,
                    operator_export_type,
                    not verbose,
                    val_keep_init_as_ip,
                    custom_opsets,
                    val_add_node_names,
                    model_file_location,
                    node_attr_to_name,
                )
            # insert function_proto into model_proto.
            proto = onnx_proto_utils._add_onnxscript_fn(
                proto,
                custom_opsets,
            )
            if verbose:
                _C._jit_onnx_log("Exported graph: ", graph)
            onnx_proto_utils._export_file(proto, f, export_map)
    finally:
        if not GLOBALS.in_onnx_export:
            raise AssertionError("GLOBALS.in_onnx_export must be True")
        GLOBALS.in_onnx_export = False
        GLOBALS.autograd_inlining = _autograd_inlining_previous
        _reset_trace_module_map()

    return torch_out

