import functools
from typing import Any

def _register_propagate_rule(
    aten_op: torch._ops.OpOverload | Sequence[torch._ops.OpOverload],
    handler: _HandlerType,
) -> _HandlerType:
    if not isinstance(aten_op, (list, tuple)):
        aten_op = [aten_op]  # type: ignore[assignment, list-item]

    assert isinstance(aten_op, (list, tuple)), f"{type(aten_op)=}"
    for op in aten_op:
        assert isinstance(op, torch._ops.OpOverload)
        propagate_rules[op] = handler
    return handler


def _register_propagate_rule(
    aten_op: torch._ops.OpOverload | Sequence[torch._ops.OpOverload],
    handler: _HandlerType,
) -> _HandlerType:
    if not isinstance(aten_op, (list, tuple)):
        aten_op = [aten_op]  # type: ignore[assignment, list-item]

    @functools.wraps(handler)
    def wrapper(node: Node, *args: Any, **kwargs: Any) -> PropagateStatus:
        fwd_bwd_status = handler(node, *args, **kwargs)
        if isinstance(fwd_bwd_status, PropagateStatus):
            return fwd_bwd_status
        assert isinstance(fwd_bwd_status, (list, tuple)) and len(fwd_bwd_status) == 2
        fwd_status, bwd_status = fwd_bwd_status
        log.debug(
            "Chunking metadata propagation for %s: Fwd status %s, bwd status %s",
            node,
            fwd_status,
            bwd_status,
        )
        if fwd_status == PropagateStatus.FAIL or bwd_status == PropagateStatus.FAIL:
            return PropagateStatus.FAIL
        if (
            fwd_status == PropagateStatus.SUCCEED_WITH_CHANGE
            or bwd_status == PropagateStatus.SUCCEED_WITH_CHANGE
        ):
            return PropagateStatus.SUCCEED_WITH_CHANGE
        return PropagateStatus.SUCCEED_NO_CHANGE

    assert isinstance(aten_op, (list, tuple)), f"{type(aten_op)=}"
    for op in aten_op:
        assert isinstance(op, torch._ops.OpOverload)
        propagate_rules[op] = wrapper
    return wrapper

