
def split_blocks_at_uninits(
    blocks: list[BasicBlock], pre_must_defined: AnalysisDict[Value], strict_traceback_checks: bool
) -> list[BasicBlock]:
    new_blocks: list[BasicBlock] = []

    init_registers = []
    init_registers_set = set()
    bitmap_registers: list[Register] = []  # Init status bitmaps
    bitmap_backed: list[Register] = []  # These use bitmaps to track init status

    # First split blocks on ops that may raise.
    for block in blocks:
        ops = block.ops
        block.ops = []
        cur_block = block
        new_blocks.append(cur_block)

        for i, op in enumerate(ops):
            defined = pre_must_defined[block, i]
            for src in op.unique_sources():
                # If a register operand is not guaranteed to be
                # initialized is an operand to something other than a
                # check that it is defined, insert a check.

                # Note that for register operand in a LoadAddress op,
                # we should be able to use it without initialization
                # as we may need to use its address to update itself
                if (
                    isinstance(src, Register)
                    and src not in defined
                    and not (isinstance(op, Branch) and op.op == Branch.IS_ERROR)
                    and not isinstance(op, LoadAddress)
                ):
                    if src not in init_registers_set:
                        init_registers.append(src)
                        init_registers_set.add(src)

                    # XXX: if src.name is empty, it should be a
                    # temp... and it should be OK??
                    if not src.name:
                        continue

                    new_block, error_block = BasicBlock(), BasicBlock()
                    new_block.error_handler = error_block.error_handler = cur_block.error_handler
                    new_blocks += [error_block, new_block]

                    if not src.type.error_overlap:
                        cur_block.ops.append(
                            Branch(
                                src,
                                true_label=error_block,
                                false_label=new_block,
                                op=Branch.IS_ERROR,
                                line=op.line,
                            )
                        )
                    else:
                        # We need to use bitmap for this one.
                        check_for_uninit_using_bitmap(
                            cur_block.ops,
                            src,
                            bitmap_registers,
                            bitmap_backed,
                            error_block,
                            new_block,
                            op.line,
                        )

                    if strict_traceback_checks:
                        assert (
                            op.line >= 0
                        ), f"Cannot raise an error with a negative line number for op {op}"
                    raise_std = RaiseStandardError(
                        RaiseStandardError.UNBOUND_LOCAL_ERROR,
                        f'local variable "{src.name}" referenced before assignment',
                        op.line,
                    )
                    error_block.ops.append(raise_std)
                    error_block.ops.append(Unreachable())
                    cur_block = new_block
            cur_block.ops.append(op)

    if bitmap_backed:
        update_register_assignments_to_set_bitmap(new_blocks, bitmap_registers, bitmap_backed)

    if init_registers:
        new_ops: list[Op] = []
        for reg in init_registers:
            err = LoadErrorValue(reg.type, undefines=True)
            new_ops.append(err)
            new_ops.append(Assign(reg, err))
        for reg in bitmap_registers:
            new_ops.append(Assign(reg, Integer(0, bitmap_rprimitive)))
        new_blocks[0].ops[0:0] = new_ops

    return new_blocks

