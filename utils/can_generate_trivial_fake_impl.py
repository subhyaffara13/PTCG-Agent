
def can_generate_trivial_fake_impl(op: OpOverload) -> bool:
    if not isinstance(op, OpOverload):
        raise AssertionError(f"op must be OpOverload, got {type(op)}")
    if is_builtin(op):
        # We control the built-ins. These may (in rare cases)
        # do input metadata mutation (which we have banned on custom ops)
        return False
    schema = op._schema
    # It's suspicious if the op is not mutable but returns nothing, so we return False out of an abundance of caution
    if not schema.is_mutable:
        return False
    if len(schema.returns) > 0:
        return False
    # If the op returns nothing, then it has a trivial fake impl.
    return True

