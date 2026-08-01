
def is_accessor_node(node: torch.fx.Node) -> bool:
    """
    Helper function to determine if a node is trying to access
    a symbolic integer such as size, stride, offset or item. Currently
    primarily only used in a DCE pass to figure out purity.
    """

    # Dynamo only exercised condition
    if (
        node.op == "call_method"
        and isinstance(node.args[0], torch.fx.Node)
        and isinstance(node.args[0].meta.get("example_value"), torch.Tensor)
        and node.target in ["size", "stride", "storage_offset", "item"]
    ):
        return True

    if node.op == "call_function" and node.target in [
        torch.ops.aten.sym_size,
        torch.ops.aten.sym_size.default,
        torch.ops.aten.sym_size.int,
        torch.ops.aten.sym_stride,
        torch.ops.aten.sym_stride.default,
        torch.ops.aten.sym_stride.int,
        torch.ops.aten.sym_storage_offset,
        torch.ops.aten.sym_storage_offset.default,
        torch.ops.aten.sym_numel.default,
    ]:
        return True

    return False

