
def _get_schema(op, args, kwargs: dict | None = None) -> torch.FunctionSchema:
    if isinstance(op, torch._ops.OpOverload):
        return op._schema
    elif op == call_torchbind:
        return getattr(args[0], args[1]).schema
    elif op in _EFFECTFUL_HOPS_WITH_SCHEMA:
        extra_kwargs = kwargs or {}
        return op.gen_schema(*args, **extra_kwargs)
    else:
        raise RuntimeError(f"Unable to get schema for op {op}")

