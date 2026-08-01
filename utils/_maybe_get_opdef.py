
def _maybe_get_opdef(
    op: CustomOpDef | _ops.OpOverload | str,
) -> CustomOpDef | None:
    if isinstance(op, CustomOpDef):
        return op
    if isinstance(op, _ops.OpOverload):
        op = op._name
    if not isinstance(op, str):
        raise AssertionError(f"op must be str, got {type(op)}")
    if op in OPDEFS:
        return OPDEFS[op]
    return None

