
def format_trace_op_name(f: NativeFunction) -> str:
    # TODO: byte-for-byte compatible with old codegen behavior - should clean up
    if (
        f.func.kind() in (SchemaKind.functional, SchemaKind.out)
        or f.func.name.name.dunder_method
    ):
        # special case for *_out functions: the in-place and out-of-place ops
        # are overloaded with the same name in the JIT
        trace_name = str(f.func.name.name)
        trace_name = RENAME_TRACE.get(trace_name, trace_name)
        return OP_NAME.substitute(trace_name=trace_name)

    # otherwise, this is an in-place op and we need to emit both in- and
    # out-of-place versions
    outplace_trace_name = f.func.name.name.base
    inplace_trace_name = cpp.name(f.func)
    outplace_trace_name = RENAME_TRACE.get(outplace_trace_name, outplace_trace_name)
    inplace_trace_name = RENAME_TRACE.get(inplace_trace_name, inplace_trace_name)

    return SELECT.substitute(
        cond="tracer_state->force_outplace",
        true=OP_NAME.substitute(trace_name=outplace_trace_name),
        false=OP_NAME.substitute(trace_name=inplace_trace_name),
    )

