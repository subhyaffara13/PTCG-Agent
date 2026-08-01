
def _compute_proxy(
    tracer: _ProxyTracer, func: OpOverload, args: tuple[object, ...], out: PySymType
) -> Proxy:
    # Handle torch.sym_sum
    n_args: tuple[object, ...]
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        n_args = (
            tuple(
                (
                    get_proxy_slot(a, tracer).force().node
                    if isinstance(a, py_sym_types)
                    else a
                )
                for a in args[0]
            ),
        )
    else:
        n_args = tuple(
            (
                get_proxy_slot(a, tracer).force().node
                if isinstance(a, py_sym_types)
                else a
            )
            for a in args
        )

    # func doesn't have a __torch_function__ that Proxy can interpose, so
    # we gotta do it manually
    n_out = tracer.create_node("call_function", func, n_args, {})  # type: ignore[arg-type]
    p_out = fx.Proxy(n_out, tracer)
    set_meta(p_out, out)
    return p_out

