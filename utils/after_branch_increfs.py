
def after_branch_increfs(
    label: BasicBlock,
    pre_live: AnalysisDict[Value],
    pre_borrow: AnalysisDict[Value],
    source_borrowed: set[Value],
    ordering: dict[Value, int],
) -> tuple[Value, ...]:
    target_pre_live = pre_live[label, 0]
    target_borrowed = pre_borrow[label, 0]
    incref = (source_borrowed - target_borrowed) & target_pre_live
    if incref:
        return tuple(
            reg for reg in sorted(incref, key=lambda r: ordering[r]) if reg.type.is_refcounted
        )
    return ()

