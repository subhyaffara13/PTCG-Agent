
def _is_custom_op(op: "OperatorBase") -> bool:
    return not _is_aten_op(op)

