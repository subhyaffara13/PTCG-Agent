
def check_func_ir(fn: FuncIR) -> list[FnError]:
    """Applies validations to a given function ir and returns a list of errors found."""
    errors = []

    op_set = set()

    for block in fn.blocks:
        if not block.terminated:
            errors.append(
                FnError(source=block.ops[-1] if block.ops else block, desc="Block not terminated")
            )
        for op in block.ops[:-1]:
            if isinstance(op, ControlOp):
                errors.append(FnError(source=op, desc="Block has operations after control op"))

            if op in op_set:
                errors.append(FnError(source=op, desc="Func has a duplicate op"))
            op_set.add(op)

    errors.extend(check_op_sources_valid(fn))
    if errors:
        return errors

    op_checker = OpChecker(fn)
    for block in fn.blocks:
        for op in block.ops:
            op.accept(op_checker)

    return op_checker.errors

