from typing import Any

def _find_input_for_invalid_output(
    node: fx.Node,
    env: dict[fx.Node, Any],
) -> fx.Node | None:
    """Try to find a valid input replacement for an invalid forward output.

    This handles cases where a forward output depends on backward nodes but
    semantically aliases an input. For example, a view of a getitem from a
    triton kernel that mutates a buffer in backward, or a direct getitem from
    such a higher-order op. The original input may be a primal or a valid
    intermediate node already present in the forward graph.
    """
    # Pattern 1: view/reshape(getitem(ho_op, key)) -> ho_op.kwargs["kwargs"][key]
    original_input = _is_copy_node_bw_only(node)
    if (
        original_input is not None
        and original_input in env
        and not isinstance(env[original_input], InvalidNodeBase)
    ):
        return env[original_input]
    # Pattern 2: getitem(ho_op, key) -> ho_op.kwargs["kwargs"][key]
    original_input = _get_ho_op_original_input(node)
    if (
        original_input is not None
        and original_input in env
        and not isinstance(env[original_input], InvalidNodeBase)
    ):
        return env[original_input]
    return None

