
def _has_valid_out_variant_returns(
    schema: torch._C.FunctionSchema,
    mutable_args: list[torch._C.Argument],
) -> bool:
    """Out variant must return either nothing or the mutable args themselves."""
    if len(schema.returns) == 0:
        return True

    if len(schema.returns) != len(mutable_args):
        return False

    # Each return must alias exactly one mutable arg, in order
    for ret, arg in zip(schema.returns, mutable_args):
        if ret.alias_info is None or arg.alias_info is None:
            return False
        if ret.alias_info.before_set != arg.alias_info.before_set:
            return False
    return True

