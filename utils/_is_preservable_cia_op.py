
def _is_preservable_cia_op(op: "OperatorBase") -> bool:
    return _check_valid_to_preserve(op) and _is_cia_op(op)

