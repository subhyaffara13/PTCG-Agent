
def _split_decomp_table_to_cia_and_python_decomp(
    decomp_table: dict[torch._ops.OperatorBase, Callable],
) -> tuple[dict[torch._ops.OperatorBase, Callable], ...]:
    all_preservable_cia_ops = set(_collect_all_valid_cia_ops())
    cia_ops_to_callable = {}

    for op in list(decomp_table.keys()):
        # TODO we are silently allowing non-safe(non-functional) ops through a crack
        # due to core aten decomp table having non-functional entries. Once we have
        # a tighter check around core aten decomp, we should warn users about them.
        # Tracking issue: (https://github.com/pytorch/pytorch/issues/135759)

        # if it is a valid CIA op we can mess with in export, we check if it is:
        #  1. Has been marked as to be decomposed. Example:
        #        decomp_table = decomp_table_to_core_aten()
        #        del decomp_table[aten.linear]
        #     In this case, user says decompose everything except for aten.linear
        #  2. Has been marked with custom decomp behaviour. Example:
        #        decomp_table = {aten.linear: some_op}
        # For (1), we want to remove all the CIA ops that weren't handled by user as
        # it suggests they are safe to decompose, so we should remove from preservable_list.
        # for (2), we just plumb the custom decomp to AOTDIspatcher.
        # In both cases, we want to remove this CIA op from the decomp_table as it is special
        # handled.
        if op in all_preservable_cia_ops:
            cia_ops_to_callable[op] = decomp_table[op]
            all_preservable_cia_ops.remove(op)
            del decomp_table[op]
        # If it is a custom op, we want to still preserve or do whatever
        # with it if it is a functional CIA. The reason we don't remove
        # from CIA list is because we don't query custom ops.
        elif _is_preservable_cia_op(op):
            op_name = op.name()
            if op_name.startswith("aten"):
                raise AssertionError(
                    f"This should be a custom op, got aten op: {op_name}"
                )
            cia_ops_to_callable[op] = decomp_table[op]

    # If we reached here, it means user intentionally deleted these CIA ops from
    # decomp table.
    for k in all_preservable_cia_ops:
        cia_ops_to_callable[k] = _special_op_to_preserve_cia

    return cia_ops_to_callable, decomp_table

