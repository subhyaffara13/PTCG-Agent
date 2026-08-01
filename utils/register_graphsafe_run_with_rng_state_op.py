
def register_graphsafe_run_with_rng_state_op():
    class GraphSafeRunWithRngState(HigherOrderOperator):
        def __init__(self):
            super().__init__("graphsafe_run_with_rng_state")

        def __call__(self, op, *args, rng_state=None, **kwargs):
            # pyrefly: ignore [missing-attribute]
            return super().__call__(op, *args, rng_state=rng_state, **kwargs)

    graphsafe_run_with_rng_state = GraphSafeRunWithRngState()

    graphsafe_run_with_rng_state.py_impl(DispatchKey.Autograd)(
        autograd_not_implemented(graphsafe_run_with_rng_state, deferred_error=True)
    )

    @graphsafe_run_with_rng_state.py_impl(DispatchKey.CUDA)
    def impl_cuda(op, *args, rng_state=None, **kwargs):
        # pyrefly: ignore [missing-attribute]
        device_idx = rng_state.device.index
        generator = torch.cuda.default_generators[device_idx]
        current_state = generator.graphsafe_get_state()

        generator.graphsafe_set_state(rng_state)
        out = op(*args, **kwargs)
        generator.graphsafe_set_state(current_state)
        return out

    @graphsafe_run_with_rng_state.py_impl(DispatchKey.BackendSelect)
    def impl_backend_select(op, *args, rng_state=None, **kwargs):
        device = get_device(args, kwargs)
        if device != "cuda":
            raise AssertionError(
                f"GraphSafe RNG operations only supported for CUDA, got {device}"
            )
        return impl_cuda(op, *args, rng_state=rng_state, **kwargs)

    @graphsafe_run_with_rng_state.py_impl(FakeTensorMode)
    def impl_fake_tensor_mode(mode, op, *args, rng_state=None, **kwargs):
        with mode:
            return op(*args, **kwargs)

    @graphsafe_run_with_rng_state.py_impl(ProxyTorchDispatchMode)
    def impl_proxy_dispatch_mode(mode, op, *args, rng_state=None, **kwargs):
        with disable_proxy_modes_tracing():
            out = graphsafe_run_with_rng_state(op, *args, rng_state=rng_state, **kwargs)
        proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, (op, *args))
        proxy_kwargs = pytree.tree_map(
            mode.tracer.unwrap_proxy, {"rng_state": rng_state, **kwargs}
        )
        out_proxy = mode.tracer.create_proxy(
            "call_function", graphsafe_run_with_rng_state, proxy_args, proxy_kwargs
        )
        return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)

    @graphsafe_run_with_rng_state.py_functionalize_impl
    def impl_functional(ctx, op, *args, rng_state=None, **kwargs):
        unwrapped_rng_state = (
            ctx.unwrap_tensors(rng_state) if rng_state is not None else None
        )
        unwrapped_args = ctx.unwrap_tensors(args)
        unwrapped_kwargs = ctx.unwrap_tensors(kwargs)

        with ctx.redispatch_to_next():
            out = graphsafe_run_with_rng_state(
                op, *unwrapped_args, rng_state=unwrapped_rng_state, **unwrapped_kwargs
            )
            return ctx.wrap_tensors(out)

    return graphsafe_run_with_rng_state

