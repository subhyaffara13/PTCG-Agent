
def _is_view_op(tgt):
    if not isinstance(tgt, torch._ops.OpOverload):
        raise AssertionError(f"Expected torch._ops.OpOverload, got {type(tgt)}")
    # Don't apply the view optimization to any `CompositeImplicitAutograd` ops.
    # See issue: https://github.com/pytorch/pytorch/issues/133421
    if torch._C._dispatch_has_kernel_for_dispatch_key(
        tgt.name(), torch.DispatchKey.CompositeImplicitAutograd
    ):
        return False
    schema = tgt._schema
    if len(schema.arguments) > 0:
        first_arg = schema.arguments[0]
        # check if op is a view
        return first_arg.alias_info is not None and not first_arg.alias_info.is_write


def _is_view_op(tgt):
    if tgt is not None and isinstance(tgt, torch._ops.OpOverload):
        schema = tgt._schema
        if len(schema.arguments) > 0:
            first_arg = schema.arguments[0]
            # check if op is a view
            return (
                first_arg.alias_info is not None and not first_arg.alias_info.is_write
            )

