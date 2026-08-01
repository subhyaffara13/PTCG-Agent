
def _supports_delitem_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(value, DELITEM_METHOD)

