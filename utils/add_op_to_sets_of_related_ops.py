
def add_op_to_sets_of_related_ops(
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]],
    op: NSNodeTargetType,
    related_op: NSNodeTargetType | None,
) -> None:
    if related_op is not None:
        for set_of_related_ops in base_name_to_sets_of_related_ops.values():
            if related_op in set_of_related_ops:
                set_of_related_ops.add(op)
                return
        # if we got here, related_op was not found
        raise AssertionError(f"{related_op} was not found")
    else:
        counter = 0
        while str(counter) in base_name_to_sets_of_related_ops:
            counter += 1
        base_name_to_sets_of_related_ops[str(counter)] = {op}

