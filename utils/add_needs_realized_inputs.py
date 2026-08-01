
def add_needs_realized_inputs(
    fn: Collection[torch._ops.OpOverload | torch._ops.OpOverloadPacket]
    | torch._ops.OpOverload
    | torch._ops.OpOverloadPacket,
) -> list[Any] | None:
    if isinstance(fn, (list, set, tuple, OrderedSet)):  # noqa: set_linter
        # pyrefly: ignore [bad-argument-type]
        return [add_needs_realized_inputs(x) for x in fn]
    if isinstance(fn, torch._ops.OpOverload):
        needs_realized_inputs.add(fn)
    elif isinstance(fn, torch._ops.OpOverloadPacket):
        needs_realized_inputs.update(
            getattr(fn, overload) for overload in fn.overloads()
        )
    return None

