
def _is_list_op(op: OpOverload) -> bool:
    """Returns True if op is a foreach, amp_foreach, or fused op."""
    name = op.name()
    return name.startswith(("aten::_foreach_", "aten::_amp_foreach_", "aten::_fused_"))

