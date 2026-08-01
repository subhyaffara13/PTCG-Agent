
def _export_to_aten_ir(
    mod: torch.nn.Module,
    fake_args,
    fake_kwargs,
    fake_params_buffers,
    constant_attrs: ConstantAttrMap,
    produce_guards_callback=None,
    *,
    transform=lambda x: x,  # TODO(zhxchen17) Revisit if this is needed later.
    pre_dispatch=False,
    decomp_table=None,
    _prettify_placeholder_names: bool = True,
    decompose_custom_triton_ops: bool = False,
) -> ATenExportArtifact:
    custom_triton_ops_decomposition_ctx = (
        nullcontext
        if decompose_custom_triton_ops
        else _disable_custom_triton_op_functional_decomposition
    )
    # This _reparameterize_module makes sure inputs and module.params/buffers have the same fake_mode,
    # otherwise aot_export_module will error out because it sees a mix of fake_modes.
    # And we want aot_export_module to use the fake_tensor mode in dynamo to keep the pipeline easy to reason about.
    with ExitStack() as stack:
        stack.enter_context(
            torch.nn.utils.stateless._reparametrize_module(
                mod,
                fake_params_buffers,
                tie_weights=True,
                strict=True,
                stack_weights=True,
            )
        )
        stack.enter_context(_ignore_backend_decomps())
        stack.enter_context(_compiling_state_context())
        stack.enter_context(custom_triton_ops_decomposition_ctx())
        stack.enter_context(torch.no_grad())

        gm, graph_signature = transform(_aot_export_joint_with_descriptors)(
            stack,
            mod,
            fake_args,
            kwargs=fake_kwargs,
            decompositions=decomp_table,
            fake_params_buffers=fake_params_buffers,
            _record_nn_module_stack=True,
        )

    def _maybe_fixup_gm_and_output_node_meta(old_gm, new_gm):
        if isinstance(old_gm, torch.fx.GraphModule):
            if hasattr(old_gm, "meta"):
                new_gm.meta.update(old_gm.meta)
            old_output_node = list(old_gm.graph.nodes)[-1]
            new_output_node = list(new_gm.graph.nodes)[-1]
            if old_output_node.op != "output" or new_output_node.op != "output":
                raise AssertionError(
                    f"expected both output nodes to have op='output', got old={old_output_node.op!r}, new={new_output_node.op!r}"
                )
            # make sure we don't override any meta
            if "desc" in new_output_node.meta:
                del new_output_node.meta["desc"]
            new_output_node.meta.update(old_output_node.meta)

    # TODO unfortunately preserving graph-level metadata and output node's meta
    # is not working well with aot_export. So we manually copy it.
    # (The node-level meta is addressed above.)
    _maybe_fixup_gm_and_output_node_meta(mod, gm)

    # Run produce guards before we handle runtime asserts.
    # This means we run the export solver before the runtime asserts pass.
    # Right now this doesn't mean much - the export solver is only there for suggested fixes,
    # and we won't even get to constraint solving if that's needed.
    # But if in future we want to control what runtime asserts are emitted for export,
    # or rely on produce_guards + solver for some simplification on runtime asserts, this probably makes sense.
    if produce_guards_callback:
        try:
            produce_guards_callback(gm)
        except (ConstraintViolationError, ValueRangeError) as e:
            raise UserError(UserErrorType.CONSTRAINT_VIOLATION, str(e))  # noqa: B904

    return _produce_aten_artifact(
        gm=gm,
        mod=mod,
        constant_attrs=constant_attrs,
        graph_signature=graph_signature,
        pre_dispatch=pre_dispatch,
        fake_args=fake_args,
        fake_kwargs=fake_kwargs,
        fake_params_buffers=fake_params_buffers,
        _prettify_placeholder_names=_prettify_placeholder_names,
    )

