
def _get_schema_from_target(target):
    if isinstance(target, torch._ops.OpOverload):
        return target._schema
    elif type(target) in _serialization_registry:
        return _serialization_registry[type(target)].op_schema(target)
    raise RuntimeError(f"Cannot find schema for {type(target)}")

