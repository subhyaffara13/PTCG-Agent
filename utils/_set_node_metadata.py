
def _set_node_metadata(fx_node: torch.fx.Node, ir_node: ir.Node) -> None:
    """Adds namespace and other node metadata to the ONNX node."""
    namespace, class_hierarchy, name_scopes = _get_node_namespace(fx_node)
    ir_node.metadata_props["namespace"] = namespace
    ir_node.metadata_props["pkg.torch.onnx.class_hierarchy"] = repr(class_hierarchy)
    ir_node.metadata_props["pkg.torch.onnx.name_scopes"] = repr(name_scopes)
    ir_node.metadata_props["pkg.torch.onnx.fx_node"] = str(fx_node.format_node())
    ir_node.metadata_props["pkg.torch.onnx.stack_trace"] = fx_node.meta.get(
        "stack_trace", ""
    )

