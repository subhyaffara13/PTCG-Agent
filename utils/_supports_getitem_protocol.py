
def _supports_getitem_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(value, GETITEM_METHOD)

