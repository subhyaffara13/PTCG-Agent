
def is_typing_member(node: nodes.NodeNG, names_to_check: tuple[str, ...]) -> bool:
    """Check if `node` is a member of the `typing` module and has one of the names from
    `names_to_check`.
    """
    match node:
        case nodes.Name():
            try:
                import_from = node.lookup(node.name)[1][0]
            except IndexError:
                return False

            match import_from:
                case nodes.ImportFrom(modname="typing"):
                    return import_from.real_name(node.name) in names_to_check
            return False
        case nodes.Attribute():
            match safe_infer(node.expr):
                case nodes.Module(name="typing"):
                    return node.attrname in names_to_check
            return False
    return False

