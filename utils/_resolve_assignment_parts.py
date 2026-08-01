
def _resolve_assignment_parts(parts, assign_path, context):
    """Recursive function to resolve multiple assignments."""
    assign_path = assign_path[:]
    index = assign_path.pop(0)
    for part in parts:
        assigned = None
        if isinstance(part, nodes.Dict):
            # A dictionary in an iterating context
            try:
                assigned, _ = part.items[index]
            except IndexError:
                return

        elif hasattr(part, "getitem"):
            index_node = nodes.Const(index)
            try:
                assigned = part.getitem(index_node, context)
            except (AstroidTypeError, AstroidIndexError):
                return

        if not assigned:
            return

        if not assign_path:
            # we achieved to resolved the assignment path, don't infer the
            # last part
            yield assigned
        elif isinstance(assigned, util.UninferableBase):
            return
        else:
            # we are not yet on the last part of the path search on each
            # possibly inferred value
            try:
                yield from _resolve_assignment_parts(
                    assigned.infer(context), assign_path, context
                )
            except InferenceError:
                return

