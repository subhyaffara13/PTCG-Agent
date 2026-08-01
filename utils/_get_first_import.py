
def _get_first_import(
    node: ImportNode,
    context: nodes.LocalsDictNodeNG,
    name: str,
    base: str | None,
    level: int | None,
    alias: str | None,
) -> tuple[nodes.Import | nodes.ImportFrom | None, str | None]:
    """Return the node where [base.]<name> is imported or None if not found."""
    fullname = f"{base}.{name}" if base else name

    first = None
    found = False
    msg = "reimported"

    for first in context.body:
        if first is node:
            continue
        if first.scope() is node.scope() and first.fromlineno > node.fromlineno:
            continue
        if isinstance(first, nodes.Import):
            if any(fullname == iname[0] for iname in first.names):
                found = True
                break
            for imported_name, imported_alias in first.names:
                if not imported_alias and imported_name == alias:
                    found = True
                    msg = "shadowed-import"
                    break
            if found:
                break
        elif isinstance(first, nodes.ImportFrom):
            if level == first.level:
                for imported_name, imported_alias in first.names:
                    if fullname == f"{first.modname}.{imported_name}":
                        found = True
                        break
                    if (
                        name != "*"
                        and name == imported_name
                        and not (alias or imported_alias)
                    ):
                        found = True
                        break
                    if not imported_alias and imported_name == alias:
                        found = True
                        msg = "shadowed-import"
                        break
                if found:
                    break
    if found and not astroid.are_exclusive(first, node):
        return first, msg
    return None, None

