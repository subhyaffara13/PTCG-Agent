
def in_type_checking_block(node: nodes.NodeNG) -> bool:
    """Check if a node is guarded by a TYPE_CHECKING guard."""
    for ancestor in node.node_ancestors():
        if not isinstance(ancestor, nodes.If):
            continue
        if isinstance(ancestor.test, nodes.Name):
            if ancestor.test.name != "TYPE_CHECKING":
                continue
            lookup_result = ancestor.test.lookup(ancestor.test.name)[1]
            if not lookup_result:
                return False
            maybe_import_from = lookup_result[0]
            if (
                isinstance(maybe_import_from, nodes.ImportFrom)
                and maybe_import_from.modname == "typing"
            ):
                return True
            match safe_infer(ancestor.test):
                case nodes.Const(value=False):
                    return True
        elif isinstance(ancestor.test, nodes.Attribute):
            if ancestor.test.attrname != "TYPE_CHECKING":
                continue
            match safe_infer(ancestor.test.expr):
                case nodes.Module(name="typing"):
                    return True

    return False

