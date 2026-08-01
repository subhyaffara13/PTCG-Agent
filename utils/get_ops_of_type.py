
def get_ops_of_type(
    root: OpView | Operation | Module, op_class: type[OpView] | None = None
) -> list[OpView]:
    """Return all operations of the given type in the operation tree.

    Args:
      root: The operation or module to start traversing from.
      op_class: The OpView subclass to filter by (e.g. func.FuncOp). If None,
        collects all operations in the tree.

    Returns:
      A list of operations of the given type.
    """
    op = root.operation if isinstance(root, Module) else root
    ops = []

    def collect_ops(op: Operation):
        ops.append(op.opview)
        return WalkResult.ADVANCE

    op.walk(collect_ops, op_class=op_class)
    return ops

