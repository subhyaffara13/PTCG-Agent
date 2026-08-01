
def supports_delitem(value: nodes.NodeNG, _: nodes.NodeNG) -> bool:
    return _supports_protocol(value, _supports_delitem_protocol)

