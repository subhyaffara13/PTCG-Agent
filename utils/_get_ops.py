
def _get_ops(state_inst, op_classes, **options):
    # Try to get operator instances from the state INSTANCE.
    # If this fails, just return the classes
    try:
        ret = state_inst._state_to_operators(op_classes, **options)
    except NotImplementedError:
        if isinstance(op_classes, (set, tuple, frozenset)):
            ret = tuple(_make_default(x) for x in op_classes)
        else:
            ret = _make_default(op_classes)

    if isinstance(ret, set) and len(ret) == 1:
        return ret[0]

    return ret

