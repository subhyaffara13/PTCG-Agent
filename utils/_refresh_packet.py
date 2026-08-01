
def _refresh_packet(packet):
    op, overload_names = _get_packet(packet._qualified_op_name, packet._op.__module__)
    if op is None:
        raise AssertionError(f"failed to get packet for {packet._qualified_op_name}")
    packet._op = op
    packet._overload_names = overload_names

