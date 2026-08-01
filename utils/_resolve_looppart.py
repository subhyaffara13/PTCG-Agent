
def _resolve_looppart(parts, assign_path, context):
    """Recursive function to resolve multiple assignments on loops."""
    assign_path = assign_path[:]
    index = assign_path.pop(0)
    for part in parts:
        if isinstance(part, util.UninferableBase):
            continue
        if not hasattr(part, "itered"):
            continue
        try:
            itered = part.itered()
        except TypeError:
            continue
        try:
            if isinstance(itered[index], (nodes.Const, nodes.Name)):
                itered = [part]
        except IndexError:
            pass
        for stmt in itered:
            index_node = nodes.Const(index)
            try:
                assigned = stmt.getitem(index_node, context)
            except (AttributeError, AstroidTypeError, AstroidIndexError):
                continue
            if not assign_path:
                # we achieved to resolved the assignment path,
                # don't infer the last part
                yield assigned
            elif isinstance(assigned, util.UninferableBase):
                break
            else:
                # we are not yet on the last part of the path
                # search on each possibly inferred value
                try:
                    yield from _resolve_looppart(
                        assigned.infer(context), assign_path, context
                    )
                except InferenceError:
                    break

