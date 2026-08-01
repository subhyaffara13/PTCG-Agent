
def _should_decompose_because_unsafe_op(op: torch._ops.OperatorBase) -> bool:
    """
    Returns True if the op must always decompose in export/compile tracing system

    In export, we always decompose certain CIA ops that are tagged with
    maybe_aliasing_or_mutating because we statically need to know if the op is
    mutating or not. But these CIA ops could have different behaviour in runtime.

    native_batch_norm is a prim op which has a wrong schema and it needs to be replaced
    with correct schema. But until then, we will force decompose it via this tag.
    """
    if not isinstance(op, torch._ops.OpOverload):
        return False
    if torch.Tag.maybe_aliasing_or_mutating in op.tags:
        return True
    return op is torch.ops.aten.native_batch_norm.default

