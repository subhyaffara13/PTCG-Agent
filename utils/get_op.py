
def get_op(qualname):
    def error_not_found():
        raise ValueError(
            f"Could not find the operator {qualname}. Please make sure you have "
            f"already registered the operator and (if registered from C++) "
            f"loaded it via torch.ops.load_library."
        )

    ns, name = parse_qualname(qualname)
    if not hasattr(torch.ops, ns):
        error_not_found()
    opnamespace = getattr(torch.ops, ns)
    if not hasattr(opnamespace, name):
        error_not_found()
    packet = getattr(opnamespace, name)
    if not hasattr(packet, "default"):
        error_not_found()
    return packet.default

