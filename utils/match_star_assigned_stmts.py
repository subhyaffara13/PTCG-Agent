
def match_star_assigned_stmts(
    self: nodes.MatchStar,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG]:
    """Return empty generator (return -> raises StopIteration) so inferred value
    is Uninferable.
    """
    return
    yield

