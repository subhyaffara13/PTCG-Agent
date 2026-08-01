
def _match_constraint(
    node: _NameNodes, expr: nodes.NodeNG, invert: bool = False
) -> Iterator[Constraint]:
    """Yields all constraint patterns for node that match."""
    for constraint_cls in ALL_CONSTRAINT_CLASSES:
        constraint = constraint_cls.match(node, expr, invert)
        if constraint:
            yield constraint

