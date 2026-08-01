
def adjust_error_kinds(block: BasicBlock) -> None:
    """Infer more precise error_kind attributes for ops.

    We have access here to more information than what was available
    when the IR was initially built.
    """
    for op in block.ops:
        if isinstance(op, GetAttr):
            if op.class_type.class_ir.is_always_defined(op.attr):
                op.error_kind = ERR_NEVER
        if isinstance(op, SetAttr):
            if op.class_type.class_ir.is_always_defined(op.attr):
                op.error_kind = ERR_NEVER

