
def transform_block(builder: IRBuilder, block: Block) -> None:
    if not block.is_unreachable:
        builder.block_reachable_stack.append(True)
        for stmt in block.body:
            builder.accept(stmt)
            if not builder.block_reachable_stack[-1]:
                # The rest of the block is unreachable, so skip it
                break
        builder.block_reachable_stack.pop()
    # Raise a RuntimeError if we hit a non-empty unreachable block.
    # Don't complain about empty unreachable blocks, since mypy inserts
    # those after `if MYPY`.
    elif block.body:
        builder.add(
            RaiseStandardError(
                RaiseStandardError.RUNTIME_ERROR, "Reached allegedly unreachable code!", block.line
            )
        )
        builder.add(Unreachable())


def transform_block(
    block: BasicBlock,
    pre_live: AnalysisDict[Value],
    post_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    post_must_defined: AnalysisDict[Value],
) -> None:
    old_ops = block.ops
    ops: list[Op] = []
    for i, op in enumerate(old_ops):
        key = (block, i)

        assert op not in pre_live[key]
        dest = op.dest if isinstance(op, Assign) else op
        stolen = op.stolen()

        # Incref any references that are being stolen that stay live, were borrowed,
        # or are stolen more than once by this operation.
        for j, src in enumerate(stolen):
            if src in post_live[key] or src in pre_borrow[key] or src in stolen[:j]:
                maybe_append_inc_ref(ops, src)
                # For assignments to registers that were already live,
                # decref the old value.
                if dest not in pre_borrow[key] and dest in pre_live[key]:
                    assert isinstance(op, Assign), op
                    maybe_append_dec_ref(ops, dest, post_must_defined, key)

        # Strip KeepAlive. Its only purpose is to help with this transform.
        if not isinstance(op, KeepAlive):
            ops.append(op)

        # Control ops don't have any space to insert ops after them, so
        # their inc/decrefs get inserted by insert_branch_inc_and_decrefs.
        if isinstance(op, ControlOp):
            continue

        for src in op.unique_sources():
            # Decrement source that won't be live afterwards.
            if src not in post_live[key] and src not in pre_borrow[key] and src not in stolen:
                maybe_append_dec_ref(ops, src, post_must_defined, key)
        # Decrement the destination if it is dead after the op and
        # wasn't a borrowed RegisterOp
        if (
            not dest.is_void
            and dest not in post_live[key]
            and not (isinstance(op, RegisterOp) and dest.is_borrowed)
        ):
            maybe_append_dec_ref(ops, dest, post_must_defined, key)
    block.ops = ops

