
def emit_trace_body(f: NativeFunction) -> list[str]:
    trace_body: list[str] = []

    trace_body.append(format_prerecord_trace(f))

    dispatcher_sig = DispatcherSignature.from_schema(f.func)
    dispatcher_exprs = dispatcher_sig.exprs()

    # code-generated tracing kernels plumb and recompute dispatch keys directly through the kernel for performance.
    # See Note [Plumbing Keys Through The Dispatcher] for details.
    dispatch_key_set = "ks & c10::DispatchKeySet(c10::DispatchKeySet::FULL_AFTER, c10::DispatchKey::Tracer)"
    redispatch_args = ", ".join([dispatch_key_set] + [a.expr for a in dispatcher_exprs])

    assign_return_values = (
        f"{tie_return_values(f)} = "
        if f.func.kind() in [SchemaKind.functional, SchemaKind.mutable]
        and f.func.returns
        else ""
    )

    # Note that this calls the slow, dispatching variants of manual_cpp_binding ops.
    # We could probably work harder to ensure that the fast variants are
    # called instead, but the perf benefit would be minimal.
    trace_body.append(
        TRACE_DISPATCH.substitute(
            assign_return_values=assign_return_values,
            unambiguous_name=f.func.name.unambiguous_name(),
            unpacked_args=redispatch_args,
        )
    )

    trace_body.append(format_postrecord_trace(f))
    if f.func.returns:
        trace_body.append(f"return {get_return_value(f)};")
    return trace_body

