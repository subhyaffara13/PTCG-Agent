
def _is_aten_op(op: "OperatorBase") -> bool:
    return op.name().split("::")[0] == "aten"

