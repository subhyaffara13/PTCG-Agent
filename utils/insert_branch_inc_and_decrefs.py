
def insert_branch_inc_and_decrefs(
    block: BasicBlock,
    cache: BlockCache,
    blocks: list[BasicBlock],
    pre_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    post_borrow: AnalysisDict[Value],
    post_must_defined: AnalysisDict[Value],
    ordering: dict[Value, int],
) -> None:
    """Insert inc_refs and/or dec_refs after a branch/goto.

    Add dec_refs for registers that become dead after a branch.
    Add inc_refs for registers that become unborrowed after a branch or goto.

    Branches are special as the true and false targets may have a different
    live and borrowed register sets. Add new blocks before the true/false target
    blocks that tweak reference counts.

    Example where we need to add an inc_ref:

      def f(a: int) -> None
          if a:
              a = 1
          return a  # a is borrowed if condition is false and unborrowed if true
    """
    prev_key = (block, len(block.ops) - 1)
    source_live_regs = pre_live[prev_key]
    source_borrowed = post_borrow[prev_key]
    source_defined = post_must_defined[prev_key]

    term = block.terminator
    for i, target in enumerate(term.targets()):
        # HAX: After we've checked against an error value the value we must not touch the
        #      refcount since it will be a null pointer. The correct way to do this would be
        #      to perform data flow analysis on whether a value can be null (or is always
        #      null).
        omitted: Iterable[Value]
        if isinstance(term, Branch) and term.op == Branch.IS_ERROR and i == 0:
            omitted = (term.value,)
        else:
            omitted = ()

        decs = after_branch_decrefs(
            target, pre_live, source_defined, source_borrowed, source_live_regs, ordering, omitted
        )
        incs = after_branch_increfs(target, pre_live, pre_borrow, source_borrowed, ordering)
        term.set_target(i, add_block(decs, incs, cache, blocks, target))

