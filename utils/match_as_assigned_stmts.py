
def match_as_assigned_stmts(
    self: nodes.MatchAs,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG]:
    """Infer MatchAs as the Match subject if it's the only MatchCase pattern
    else raise StopIteration to yield Uninferable.
    """
    if (
        isinstance(self.parent, nodes.MatchCase)
        and isinstance(self.parent.parent, nodes.Match)
        and self.pattern is None
    ):
        yield self.parent.parent.subject

