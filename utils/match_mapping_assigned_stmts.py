
def match_mapping_assigned_stmts(
    self: nodes.MatchMapping,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG]:
    """Return empty generator (return -> raises StopIteration) so inferred value
    is Uninferable.
    """
    return
    yield

