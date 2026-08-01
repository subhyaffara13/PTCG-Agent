
def register_propagate_rule(
    aten_op: torch._ops.OpOverload | Sequence[torch._ops.OpOverload],
) -> Callable[[_HandlerType], _HandlerType]:
    return functools.partial(_register_propagate_rule, aten_op)


def register_propagate_rule(
    aten_op: torch._ops.OpOverload | Sequence[torch._ops.OpOverload],
) -> Callable[[_HandlerType], _HandlerType]:
    return functools.partial(_register_propagate_rule, aten_op)

