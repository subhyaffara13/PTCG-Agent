
def do_flag_elimination(fn: FuncIR, options: CompilerOptions) -> None:
    # Find registers that are used exactly once as source, and in a branch.
    counts: dict[Register, int] = {}
    branches: dict[Register, Branch] = {}
    labels: dict[Register, BasicBlock] = {}
    for block in fn.blocks:
        for i, op in enumerate(block.ops):
            for src in op.sources():
                if isinstance(src, Register):
                    counts[src] = counts.get(src, 0) + 1
            if i == 0 and isinstance(op, Branch) and isinstance(op.value, Register):
                branches[op.value] = op
                labels[op.value] = block

    # Based on these we can find the candidate registers.
    candidates: set[Register] = {
        r for r in branches if counts.get(r, 0) == 1 and r not in fn.arg_regs
    }

    # Remove candidates with invalid assignments.
    for block in fn.blocks:
        for i, op in enumerate(block.ops):
            if isinstance(op, Assign) and op.dest in candidates:
                next_op = block.ops[i + 1]
                if not (isinstance(next_op, Goto) and next_op.label is labels[op.dest]):
                    # Not right
                    candidates.remove(op.dest)

    builder = LowLevelIRBuilder(None, options)
    transform = FlagEliminationTransform(
        builder, {x: y for x, y in branches.items() if x in candidates}
    )
    transform.transform_blocks(fn.blocks)
    fn.blocks = builder.blocks

