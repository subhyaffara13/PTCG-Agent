
def _supports_async_iteration_protocol(value: nodes.NodeNG) -> bool:
    return _supports_protocol_method(value, AITER_METHOD)

