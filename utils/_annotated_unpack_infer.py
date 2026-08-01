
def _annotated_unpack_infer(
    stmt: nodes.NodeNG, context: InferenceContext | None = None
) -> Generator[tuple[nodes.NodeNG, SuccessfulInferenceResult]]:
    """Recursively generate nodes inferred by the given statement.

    If the inferred value is a list or a tuple, recurse on the elements.
    Returns an iterator which yields tuples in the format
    ('original node', 'inferred node').
    """
    if isinstance(stmt, (nodes.List, nodes.Tuple)):
        for elt in stmt.elts:
            inferred = utils.safe_infer(elt)
            if inferred and not isinstance(inferred, util.UninferableBase):
                yield elt, inferred
        return
    for inferred in stmt.infer(context):
        if isinstance(inferred, util.UninferableBase):
            continue
        yield stmt, inferred

