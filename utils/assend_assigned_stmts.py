from typing import Any

def assend_assigned_stmts(
    self: nodes.AssignName | nodes.AssignAttr,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    return self.parent.assigned_stmts(node=self, context=context)

