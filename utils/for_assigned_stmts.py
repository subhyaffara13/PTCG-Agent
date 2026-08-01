
def for_assigned_stmts(
    self: nodes.For | nodes.Comprehension,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if isinstance(self, nodes.AsyncFor) or getattr(self, "is_async", False):
        # Skip inferring of async code for now
        return {
            "node": self,
            "unknown": node,
            "assign_path": assign_path,
            "context": context,
        }
    if assign_path is None:
        for lst in self.iter.infer(context):
            if isinstance(lst, (nodes.Tuple, nodes.List)):
                yield from lst.elts
    else:
        yield from _resolve_looppart(self.iter.infer(context), assign_path, context)
    return {
        "node": self,
        "unknown": node,
        "assign_path": assign_path,
        "context": context,
    }

