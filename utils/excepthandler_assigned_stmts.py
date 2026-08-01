
def excepthandler_assigned_stmts(
    self: nodes.ExceptHandler,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    from astroid import objects  # pylint: disable=import-outside-toplevel

    def _generate_assigned():
        for assigned in node_classes.unpack_infer(self.type):
            if isinstance(assigned, nodes.ClassDef):
                assigned = objects.ExceptionInstance(assigned)

            yield assigned

    if isinstance(self.parent, node_classes.TryStar):
        # except * handler has assigned ExceptionGroup with caught
        # exceptions under exceptions attribute
        # pylint: disable-next=stop-iteration-return
        eg = next(
            node_classes.unpack_infer(
                extract_node(
                    """
from builtins import ExceptionGroup
ExceptionGroup
"""
                )
            )
        )
        assigned = objects.ExceptionInstance(eg)
        assigned.instance_attrs["exceptions"] = [
            nodes.List.from_elements(_generate_assigned())
        ]
        yield assigned
    else:
        yield from _generate_assigned()
    return {
        "node": self,
        "unknown": node,
        "assign_path": assign_path,
        "context": context,
    }

