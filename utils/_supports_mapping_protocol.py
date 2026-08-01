
def _supports_mapping_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(
        value, GETITEM_METHOD
    ) and _supports_protocol_method(value, KEYS_METHOD)

