
def _get_previous_field_default(node: nodes.ClassDef, name: str) -> nodes.NodeNG | None:
    """Get the default value of a previously defined field."""
    for base in reversed(node.mro()):
        if not base.is_dataclass:
            continue
        if name in base.locals:
            for assign in base.locals[name]:
                if (
                    isinstance(assign.parent, nodes.AnnAssign)
                    and assign.parent.value
                    and isinstance(assign.parent.value, nodes.Call)
                    and _looks_like_dataclass_field_call(assign.parent.value)
                ):
                    default = _get_field_default(assign.parent.value)
                    if default:
                        return default[1]
    return None

