
def _has_self_referential_shape(
    shapes: list[int | torch.fx.Node], node: torch.fx.Node
) -> bool:
    """
    Check if any shape in `shapes` depends on `node`.

    This is used to detect cycles when constant_fold_uniform_value creates a
    replacement full() node whose shape includes a sym_size computed from the
    original tensor being replaced.

    Checks direct args only - shape nodes typically come from sym_size(tensor, dim)
    where tensor is a direct arg.
    """
    for shape_node in shapes:
        if isinstance(shape_node, torch.fx.Node):
            if node in shape_node.args:
                return True
    return False

