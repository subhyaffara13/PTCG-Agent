from typing import Any, Callable

def _non_strict_export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any] | None,
    preserve_module_call_signature: tuple[str, ...],
    orig_in_spec: TreeSpec,
    prefer_deferred_runtime_asserts_over_guards: bool,
    _to_aten_func: Callable,
) -> ExportArtifact:
    """
    _to_aten_func can either be `_export_to_aten_ir_make_fx` or `_export_to_aten_ir`
    """

    out_spec: TreeSpec | None = None
    in_spec: TreeSpec | None = None

    module_call_specs: dict[str, dict[str, pytree.TreeSpec]] = {}

    def _tuplify_outputs(aot_export):
        def _aot_export_non_strict(stack, mod, args, *, kwargs=None, **flags):
            kwargs = kwargs or {}

            class Wrapper(torch.nn.Module):
                def __init__(self, mod):
                    super().__init__()
                    self._export_root = mod

                def forward(self, *args, **kwargs):
                    nonlocal out_spec
                    nonlocal in_spec
                    mod = self._export_root
                    _, in_spec = pytree.tree_flatten((args, kwargs))
                    if isinstance(mod, torch.fx.GraphModule):
                        # NOTE: We're going to run this graph module with an fx interpreter,
                        # which will not run any forward hooks. Thus, ideally, we should run
                        # all forward hooks here. But the general logic for running them is
                        # complicated (see nn/module.py), and probably not worth duplicating.
                        # Instead we only look for, and run, an export-specific forward hook.
                        if (
                            _check_input_constraints_pre_hook
                            in mod._forward_pre_hooks.values()
                        ):
                            _check_input_constraints_pre_hook(mod, args, kwargs)
                        with torch.fx.traceback.preserve_node_meta():
                            args = (*args, *kwargs.values())
                            tree_out = torch.fx.Interpreter(mod).run(*args)
                    else:
                        tree_out = mod(*args, **kwargs)
                    flat_outs, out_spec = pytree.tree_flatten(tree_out)
                    return tuple(flat_outs)

            wrapped_mod = Wrapper(mod)
            # Patch export_root to the signatures so that wrapper module correctly populates the
            # in/out spec
            new_preserved_call_signatures = [
                "_export_root." + i for i in preserve_module_call_signature
            ]
            ctx = nullcontext()
            if not isinstance(mod, torch.fx.GraphModule):
                ctx = _wrap_submodules(  # type: ignore[assignment]
                    wrapped_mod, new_preserved_call_signatures, module_call_specs
                )
            with ctx:
                gm, sig = aot_export(stack, wrapped_mod, args, kwargs=kwargs, **flags)
            log.debug("Exported program from AOTAutograd:\n%s", gm)

            sig.parameters = pytree.tree_map(_strip_root, sig.parameters)
            sig.buffers = pytree.tree_map(_strip_root, sig.buffers)
            sig.inputs_to_buffers = pytree.tree_map(_strip_root, sig.inputs_to_buffers)
            sig.inputs_to_parameters = pytree.tree_map(
                _strip_root, sig.inputs_to_parameters
            )
            sig.buffers_to_mutate = pytree.tree_map(_strip_root, sig.buffers_to_mutate)
            sig.parameters_to_mutate = pytree.tree_map(
                _strip_root, sig.parameters_to_mutate
            )

            for node in gm.graph.nodes:
                if "nn_module_stack" in node.meta:
                    nn_module_stack = node.meta["nn_module_stack"]
                    node.meta["nn_module_stack"] = {
                        _fixup_key(key): val
                        for key, val in pytree.tree_map(
                            _strip_root, nn_module_stack
                        ).items()
                    }

            return gm, sig

        return _aot_export_non_strict

    # NOTE: We need to enter _compiling_state_context() here so that FakeTensors
    # created for params/buffers are properly tracked for leak detection.
    # See detect_non_strict_fake_tensor_leaks config.
    # We only enter the context if leak detection is enabled to avoid changing
    # behavior when the config is OFF.
    _fakify_ctx = (
        _compiling_state_context()
        if torch._export.config.detect_non_strict_fake_tensor_leaks
        else nullcontext()
    )
    with _fakify_ctx:
        (
            fake_mode,
            fake_args,
            fake_kwargs,
            equalities_inputs,
            original_signature,
            dynamic_shapes,
        ) = make_fake_inputs(
            mod,
            args,
            kwargs,
            dynamic_shapes,
            prefer_deferred_runtime_asserts_over_guards=prefer_deferred_runtime_asserts_over_guards,  # for shape env initialization
        )

        fake_params_buffers = _fakify_params_buffers(fake_mode, mod)

    def _produce_guards_callback(gm):
        return produce_guards_and_solve_constraints(
            fake_mode=fake_mode,
            gm=gm,
            dynamic_shapes=dynamic_shapes,
            equalities_inputs=equalities_inputs,
            original_signature=original_signature,
        )

    tx = TracingContext(fake_mode)

    # We also need to attach dynamo configs as these will be used in HOOs that
    # use torch.compile, like cond
    dynamo_config = dataclasses.asdict(DEFAULT_EXPORT_DYNAMO_CONFIG)
    dynamo_config["do_not_emit_runtime_asserts"] = (
        False  # We want to emit runtime asserts
    )

    with (
        fake_mode,
        _NonStrictTorchFunctionHandler(),
        tracing(tx),
        torch._dynamo.config.patch(dynamo_config),
    ):
        with (
            _fakify_script_objects(mod, fake_args, fake_kwargs, fake_mode) as (
                patched_mod,
                new_fake_args,
                new_fake_kwargs,
                new_fake_constant_attrs,
                map_fake_to_real,
            ),
            _fakify_module_inputs(fake_args, fake_kwargs, fake_mode),
            _override_builtin_ops(),
        ):
            # _to_aten_func is _export_to_aten_ir when using the default non-strict export
            # We need to pass positional args correctly
            aten_export_artifact = _to_aten_func(
                patched_mod,
                new_fake_args,
                new_fake_kwargs,
                fake_params_buffers,
                new_fake_constant_attrs,
                produce_guards_callback=_produce_guards_callback,
                transform=_tuplify_outputs,
            )
            # aten_export_artifact.constants contains only fake script objects, we need to map them back
            aten_export_artifact.constants = {
                fqn: map_fake_to_real[obj] if isinstance(obj, FakeScriptObject) else obj
                for fqn, obj in aten_export_artifact.constants.items()
            }

    _move_non_persistent_buffers_to_tensor_constants(
        mod, aten_export_artifact.sig, aten_export_artifact.constants
    )

    if out_spec is None:
        raise AssertionError("out_spec must not be None")
    if in_spec is None:
        raise AssertionError("in_spec must not be None")

    return ExportArtifact(
        aten=aten_export_artifact,
        in_spec=in_spec,
        out_spec=out_spec,
        fake_mode=fake_mode,
        module_call_specs=module_call_specs,
    )

