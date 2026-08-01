
def run_analysis(
    blocks: list[BasicBlock],
    cfg: CFG,
    gen_and_kill: OpVisitor[GenAndKill[T]],
    initial: set[T],
    kind: int,
    backward: bool,
    universe: set[T] | None = None,
) -> AnalysisResult[T]:
    """Run a general set-based data flow analysis.

    Args:
        blocks: All basic blocks
        cfg: Control-flow graph for the code
        gen_and_kill: Implementation of gen and kill functions for each op
        initial: Value of analysis for the entry points (for a forward analysis) or the
            exit points (for a backward analysis)
        kind: MUST_ANALYSIS or MAYBE_ANALYSIS
        backward: If False, the analysis is a forward analysis; it's backward otherwise
        universe: For a must analysis, the set of all possible values. This is the starting
            value for the work list algorithm, which will narrow this down until reaching a
            fixed point. For a maybe analysis the iteration always starts from an empty set
            and this argument is ignored.

    Return analysis results: (before, after)
    """
    block_gen = {}
    block_kill = {}

    # Calculate kill and gen sets for entire basic blocks.
    for block in blocks:
        gen: set[T] = set()
        kill: set[T] = set()
        ops = block.ops
        if backward:
            ops = list(reversed(ops))
        for op in ops:
            opgen, opkill = op.accept(gen_and_kill)
            if opkill:
                gen -= opkill

            if opgen:
                gen |= opgen
                kill -= opgen

            if opkill:
                kill |= opkill

        block_gen[block] = gen
        block_kill[block] = kill

    # Set up initial state for worklist algorithm.
    worklist = list(blocks)
    if not backward:
        worklist.reverse()  # Reverse for a small performance improvement
    workset = set(worklist)
    before: dict[BasicBlock, set[T]] = {}
    after: dict[BasicBlock, set[T]] = {}
    for block in blocks:
        if kind == MAYBE_ANALYSIS:
            before[block] = set()
            after[block] = set()
        else:
            assert universe is not None, "Universe must be defined for a must analysis"
            before[block] = set(universe)
            after[block] = set(universe)

    if backward:
        pred_map = cfg.succ
        succ_map = cfg.pred
    else:
        pred_map = cfg.pred
        succ_map = cfg.succ

    # Run work list algorithm to generate in and out sets for each basic block.
    while worklist:
        label = worklist.pop()
        workset.remove(label)
        if pred_map[label]:
            new_before: set[T] | None = None
            for pred in pred_map[label]:
                if new_before is None:
                    new_before = set(after[pred])
                elif kind == MAYBE_ANALYSIS:
                    new_before |= after[pred]
                else:
                    new_before &= after[pred]
            assert new_before is not None
        else:
            new_before = set(initial)
        before[label] = new_before
        new_after = (new_before - block_kill[label]) | block_gen[label]
        if new_after != after[label]:
            for succ in succ_map[label]:
                if succ not in workset:
                    worklist.append(succ)
                    workset.add(succ)
        after[label] = new_after

    # Run algorithm for each basic block to generate opcode-level sets.
    op_before: dict[tuple[BasicBlock, int], set[T]] = {}
    op_after: dict[tuple[BasicBlock, int], set[T]] = {}
    for block in blocks:
        label = block
        cur = before[label]
        ops_enum: Iterator[tuple[int, Op]] = enumerate(block.ops)
        if backward:
            ops_enum = reversed(list(ops_enum))
        for idx, op in ops_enum:
            op_before[label, idx] = cur
            opgen, opkill = op.accept(gen_and_kill)
            if opkill:
                cur = cur - opkill
            if opgen:
                cur = cur | opgen
            op_after[label, idx] = cur
    if backward:
        op_after, op_before = op_before, op_after

    return AnalysisResult(op_before, op_after)

