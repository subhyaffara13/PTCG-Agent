
def unconvertible_ops(
    model,
    args,
    training: _C_onnx.TrainingMode = _C_onnx.TrainingMode.EVAL,
    opset_version: int | None = None,
) -> tuple[_C.Graph, list[str]]:
    """Returns an approximated list of all ops that are yet supported by :mod:`torch.onnx`.

    .. deprecated:: 2.5
        Unconvertible ops are not definitive. Please remove usage of this function.

    The list is approximated because some ops may be removed during the conversion
    process and don't need to be converted. Some other ops may have partial support
    that will fail conversion with particular inputs. Please open a Github Issue
    for op support requests.

    Args:
        model: Same as the `model` parameter in :func:`torch.onnx.export`.
        args: Same as the `args` parameter in :func:`torch.onnx.export`.
        training: Same as the `training` parameter in :func:`torch.onnx.export`.
        opset_version: Same as the `opset_version` parameter in :func:`torch.onnx.export`.

    Returns:
        The JIT graph and a list of unconvertible ops in the format of "domain::op".
    """

    opset_version = opset_version or _constants.ONNX_DEFAULT_OPSET
    GLOBALS.export_onnx_opset_version = opset_version

    try:
        with exporter_context(model, training, verbose=False):
            # Create a mostly clean JIT graph that contains the plain aten and
            # other ops we can check with the symbolic registry.
            # NOTE: We don't want to actually convert any ops to ONNX or run any
            # symbolic functions because there is a higher chance that a pass
            # fails or an unconvertible op messes up the graph during ONNX conversion.
            # This way we can always generate a list just by looking at the names
            # of the ops in the graph.
            args = _decide_input_format(model, args)
            model = _pre_trace_quant_model(model, args)
            graph, _, _, module = _create_jit_graph(model, args)
            _C._jit_pass_inline(graph)
            _C._jit_pass_onnx_remove_inplace_ops_for_onnx(graph, module)
            _C._jit_pass_erase_number_types(graph)
            _C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)
    except Exception as e:
        raise errors.OnnxExporterError(
            "Failed to discover unconvertible ops because of errors during the JIT graph "
            "generation process."
        ) from e

    unsupported_ops = []
    for node in graph.nodes():
        domain_op = node.kind()
        if domain_op.startswith(("onnx::", "prim::")):
            # We consider onnx and prim ops as supported ops, even though some "prim"
            # ops are not implemented as symbolic functions, because they may be
            # eliminated in the conversion passes. Users may still see errors caused
            # by prim ops even though they don't show up in the list.
            continue
        if not registration.registry.is_registered_op(
            domain_op.rstrip("_"), opset_version
        ):
            # We consider all registered ops supported, even though some of them are
            # only partially supported, because there is not yet a good way to check
            # if an op is fully supported.
            # TODO(justinchuby): Create a way to check if an op is fully supported.
            unsupported_ops.append(domain_op)
    return graph, unsupported_ops

