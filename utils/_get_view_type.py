
def _get_view_type(tgt) -> _ViewType:
    if tgt is not None and isinstance(tgt, torch._ops.OpOverload):
        schema = tgt._schema
        if len(schema.arguments) > 0:
            first_arg = schema.arguments[0]
            # check if op is a view
            if first_arg.alias_info is not None and not first_arg.alias_info.is_write:
                # check if op is a multi-output view
                if "*" in first_arg.alias_info.after_set:
                    return _ViewType.MultiOutputView
                else:
                    return _ViewType.SingleOutputView
    return _ViewType.NonView

