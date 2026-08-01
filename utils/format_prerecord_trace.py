
def format_prerecord_trace(f: NativeFunction) -> str:
    if not should_trace(f):
        return ""

    # TODO: clean up old codegen behavior
    is_inplace = (
        f.func.kind() in (SchemaKind.inplace, SchemaKind.out)
        and not f.func.name.name.dunder_method
    )
    add_args = (
        RENAME_TRACE_ADD_ARGS.get(f.func.name.name.base, "") if is_inplace else ""
    )
    additional_inputs = (
        SELECT.substitute(
            cond="tracer_state->force_outplace",
            true=add_args,
            false="",
        )
        if add_args
        else ""
    )

    return PRE_RECORD_TRACE.substitute(
        set_op_name=format_trace_op_name(f),
        add_trace_inputs=format_trace_inputs(f) + additional_inputs,
        inplace_guard=INPLACE_GUARD.substitute(
            name=cpp.name(f.func),
            mutable_input=f.func.arguments.out[0].name
            if f.func.arguments.out
            else "self",
        )
        if is_inplace
        else "",
    )

