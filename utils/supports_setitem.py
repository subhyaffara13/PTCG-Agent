
def supports_setitem(value: nodes.NodeNG, _: nodes.NodeNG) -> bool:
    return _supports_protocol(value, _supports_setitem_protocol)

