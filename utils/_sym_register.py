
def _sym_register(
    tracer: _ProxyTracer, func: OpOverload, args: tuple[object, ...], out: object
) -> None:
    # If func returned a constant, we don't need to trace; we have
    # determined that the result is constant (no matter if the inputs
    # were symbolic) and it is no longer necessary to trace the
    # computation.  This could occur if func triggered some guards.
    if isinstance(out, py_sym_types):
        p_out_thunk = thunkify(
            tracer, _compute_proxy, tracer, func=func, args=args, out=out
        )
        set_proxy_slot(out, tracer, p_out_thunk)

