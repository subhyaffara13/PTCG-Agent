
def _get_all_attribute_assignments(
    node: nodes.FunctionDef, name: str | None = None
) -> set[str]:
    attributes: set[str] = set()
    for child in node.nodes_of_class((nodes.Assign, nodes.AnnAssign)):
        targets = []
        match child:
            case nodes.Assign():
                targets = child.targets
            case nodes.AnnAssign():
                targets = [child.target]
        for assign_target in targets:
            match assign_target:
                case nodes.Tuple():
                    targets.extend(assign_target.elts)
                    continue
                case nodes.AssignAttr(expr=nodes.Name(name=n)) if (
                    n is None or n == name
                ):
                    attributes.add(assign_target.attrname)
    return attributes

