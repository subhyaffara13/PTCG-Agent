
def _find_inplace_method(inst: Instance, method: str, operator: str) -> str | None:
    if operator in operators.ops_with_inplace_method:
        inplace_method = "__i" + method[2:]
        if inst.type.has_readable_member(inplace_method):
            return inplace_method
    return None

