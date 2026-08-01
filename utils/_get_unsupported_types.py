
def _get_unsupported_types() -> tuple[type, ...]:
    # We only do ID_MATCH on C objects which is already banned from guards serialization.
    ret: tuple[type, ...] = (
        torch._C.Stream,
        weakref.ReferenceType,
    )
    try:
        ret += (torch._C._distributed_c10d.ProcessGroup,)
    except AttributeError:
        pass
    return ret

