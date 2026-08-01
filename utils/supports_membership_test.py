
def supports_membership_test(value: nodes.NodeNG) -> bool:
    supported = _supports_protocol(value, _supports_membership_test_protocol)
    return supported or is_iterable(value)

