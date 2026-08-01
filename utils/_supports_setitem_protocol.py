
def _supports_setitem_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(value, SETITEM_METHOD)

