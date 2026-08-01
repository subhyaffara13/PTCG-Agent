
def check_op_sources_valid(fn: FuncIR) -> list[FnError]:
    errors = []
    valid_ops: set[Op] = set()
    valid_registers: set[Register] = set()

    for block in fn.blocks:
        valid_ops.update(block.ops)

        for op in block.ops:
            if isinstance(op, BaseAssign):
                valid_registers.add(op.dest)
            elif isinstance(op, LoadAddress) and isinstance(op.src, Register):
                valid_registers.add(op.src)

    valid_registers.update(fn.arg_regs)

    for block in fn.blocks:
        for op in block.ops:
            for source in op.sources():
                if isinstance(source, (Integer, Float, Undef)):
                    pass
                elif isinstance(source, Op):
                    if source not in valid_ops:
                        errors.append(
                            FnError(
                                source=op,
                                desc=f"Invalid op reference to op of type {type(source).__name__}",
                            )
                        )
                elif isinstance(source, Register):
                    if source not in valid_registers:
                        errors.append(
                            FnError(
                                source=op, desc=f"Invalid op reference to register {source.name!r}"
                            )
                        )

    return errors

