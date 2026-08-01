
def _can_assign_attr(node: nodes.ClassDef, attrname: str | None) -> bool:
    try:
        slots = node.slots()
    except NotImplementedError:
        pass
    else:
        if slots and attrname not in {slot.value for slot in slots}:
            return False
    return node.qname() != "builtins.object"

