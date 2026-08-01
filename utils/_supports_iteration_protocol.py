
def _supports_iteration_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(value, ITER_METHOD) or _supports_protocol_method(
        value, GETITEM_METHOD
    )

