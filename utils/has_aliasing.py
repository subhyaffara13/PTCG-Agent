
def has_aliasing(op: OpType):
    # NOT FOR PUBLIC USE
    if isinstance(op, torch._ops.HigherOrderOperator):
        return False

    for arg in op._schema.arguments:
        if arg.alias_info is not None:
            return True
    for arg in op._schema.returns:
        if arg.alias_info is not None:
            return True
    return False

