
def get_base_name_for_op(
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]],
    op: NSNodeTargetType,
) -> str | None:
    for base_name, set_of_related_ops in base_name_to_sets_of_related_ops.items():
        if op in set_of_related_ops:
            return base_name
    return None

