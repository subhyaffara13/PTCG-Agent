
def _get_dataclass_attributes(
    node: nodes.ClassDef, init: bool = False
) -> Iterator[nodes.AnnAssign]:
    """Yield the AnnAssign nodes of dataclass attributes for the node.

    If init is True, also include InitVars.
    """
    for assign_node in node.body:
        if not (
            isinstance(assign_node, nodes.AnnAssign)
            and isinstance(assign_node.target, nodes.AssignName)
        ):
            continue

        # Annotation is never None
        if is_class_var(assign_node.annotation):  # type: ignore[arg-type]
            continue

        if _is_keyword_only_sentinel(assign_node.annotation):
            continue

        # Annotation is never None
        if not init and _is_init_var(assign_node.annotation):  # type: ignore[arg-type]
            continue

        yield assign_node

