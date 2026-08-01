
def split_blocks_at_errors(
    blocks: list[BasicBlock],
    default_error_handler: BasicBlock,
    func_name: str | None,
    strict_traceback_checks: bool,
) -> list[BasicBlock]:
    new_blocks: list[BasicBlock] = []

    # First split blocks on ops that may raise.
    for block in blocks:
        ops = block.ops
        block.ops = []
        cur_block = block
        new_blocks.append(cur_block)

        # If the block has an error handler specified, use it. Otherwise
        # fall back to the default.
        error_label = block.error_handler or default_error_handler
        block.error_handler = None

        for op in ops:
            target: Value = op
            cur_block.ops.append(op)
            if isinstance(op, RegisterOp) and op.error_kind != ERR_NEVER:
                # Split
                new_block = BasicBlock()
                new_blocks.append(new_block)

                if op.error_kind == ERR_MAGIC:
                    # Op returns an error value on error that depends on result RType.
                    variant = Branch.IS_ERROR
                    negated = False
                elif op.error_kind == ERR_FALSE:
                    # Op returns a C false value on error.
                    variant = Branch.BOOL
                    negated = True
                elif op.error_kind == ERR_ALWAYS:
                    variant = Branch.BOOL
                    negated = True
                    # this is a hack to represent the always fail
                    # semantics, using a temporary bool with value false
                    target = Integer(0, bool_rprimitive)
                elif op.error_kind == ERR_MAGIC_OVERLAPPING:
                    comp = insert_overlapping_error_value_check(cur_block.ops, target)
                    new_block2 = BasicBlock()
                    new_blocks.append(new_block2)
                    branch = Branch(
                        comp,
                        true_label=new_block2,
                        false_label=new_block,
                        op=Branch.BOOL,
                        rare=True,
                    )
                    cur_block.ops.append(branch)
                    cur_block = new_block2
                    target = primitive_call(err_occurred_op, [], target.line)
                    cur_block.ops.append(target)
                    variant = Branch.IS_ERROR
                    negated = True
                else:
                    assert False, "unknown error kind %d" % op.error_kind

                # Void ops can't generate errors since error is always
                # indicated by a special value stored in a register.
                if op.error_kind != ERR_ALWAYS:
                    assert not op.is_void, "void op generating errors?"

                branch = Branch(
                    target, true_label=error_label, false_label=new_block, op=variant, line=op.line
                )
                branch.negated = negated
                if op.line != NO_TRACEBACK_LINE_NO and func_name is not None:
                    if strict_traceback_checks:
                        assert (
                            op.line >= 0
                        ), f"Cannot add a traceback entry with a negative line number for op {op}"
                    branch.traceback_entry = (func_name, op.line)
                cur_block.ops.append(branch)
                cur_block = new_block

    return new_blocks

