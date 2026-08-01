
def after_branch_decrefs(
    label: BasicBlock,
    pre_live: AnalysisDict[Value],
    source_defined: set[Value],
    source_borrowed: set[Value],
    source_live_regs: set[Value],
    ordering: dict[Value, int],
    omitted: Iterable[Value],
) -> tuple[tuple[Value, bool], ...]:
    target_pre_live = pre_live[label, 0]
    decref = source_live_regs - target_pre_live - source_borrowed
    if decref:
        return tuple(
            (reg, is_maybe_undefined(source_defined, reg))
            for reg in sorted(decref, key=lambda r: ordering[r])
            if reg.type.is_refcounted and reg not in omitted
        )
    return ()

