
def register_run_with_rng_state_op():
    class RunWithRngState(HigherOrderOperator):
        def __init__(self):
            super().__init__("run_with_rng_state", cacheable=True)

        def __call__(self, rng_state, op, *args, **kwargs):
            # pyrefly: ignore [missing-attribute]
            return super().__call__(rng_state, op, *args, **kwargs)

    run_with_rng_state = RunWithRngState()

    run_with_rng_state.py_impl(DispatchKey.Autograd)(
        autograd_not_implemented(run_with_rng_state, deferred_error=True)
    )

    @run_with_rng_state.py_impl(DispatchKey.CUDA)
    def impl_cuda(rng_state, op, *args, **kwargs):
        current_state = torch.cuda.get_rng_state()
        torch.cuda.set_rng_state(rng_state.cpu())
        out = op(*args, **kwargs)
        torch.cuda.set_rng_state(current_state)
        return out

    @run_with_rng_state.py_impl(DispatchKey.CPU)
    def impl_cpu(rng_state, op, *args, **kwargs):
        current_state = torch.get_rng_state()
        torch.set_rng_state(rng_state)
        out = op(*args, **kwargs)
        torch.set_rng_state(current_state)
        return out

    @run_with_rng_state.py_impl(DispatchKey.HPU)
    def impl_hpu(rng_state, op, *args, **kwargs):
        if hasattr(torch, "hpu"):
            current_state = torch.hpu.get_rng_state()
            torch.hpu.set_rng_state(rng_state)
            out = op(*args, **kwargs)
            torch.hpu.set_rng_state(current_state)
            return out
        raise RuntimeError("functionalize a hpu RNG operator is not supported.")

    @run_with_rng_state.py_impl(DispatchKey.XPU)
    def impl_xpu(rng_state, op, *args, **kwargs):
        current_state = torch.xpu.get_rng_state()
        torch.xpu.set_rng_state(rng_state)
        out = op(*args, **kwargs)
        torch.xpu.set_rng_state(current_state)
        return out

    @run_with_rng_state.py_impl(ProxyTorchDispatchMode)
    def impl_proxy_dispatch_mode(mode, rng_state, op, *args, **kwargs):
        # TODO: you don't need to do this, the dispatch here already disabled
        # it
        with disable_proxy_modes_tracing():
            out = run_with_rng_state(rng_state, op, *args, **kwargs)
        proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, (rng_state, op, *args))
        proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)
        out_proxy = mode.tracer.create_proxy(
            "call_function", run_with_rng_state, proxy_args, proxy_kwargs
        )
        return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)

    @run_with_rng_state.py_impl(DispatchKey.BackendSelect)
    def impl_backend_select(rng_state, op, *args, **kwargs):
        impl_map = {
            "cuda": impl_cuda,
            "cpu": impl_cpu,
            "hpu": impl_hpu,
            "xpu": impl_xpu,
        }
        device = get_device(args, kwargs)
        if device not in impl_map:
            raise AssertionError(f"Backend not supported for {device}")
        impl = impl_map[device]
        return impl(rng_state, op, *args, **kwargs)

    @run_with_rng_state.py_impl(FakeTensorMode)
    def impl_fake_tensor_mode(mode, rng_state, op, *args, **kwargs):
        # Skip setting the set_rng_state as it does not work well with fake tensors.
        # And it does not matter for the fake tensor mode.
        with mode:
            return op(*args, **kwargs)

    @run_with_rng_state.py_functionalize_impl
    def impl_functional(ctx, rng_state, op, *args, **kwargs):
        unwrapped_rng_state = ctx.unwrap_tensors(rng_state)
        unwrapped_args = ctx.unwrap_tensors(args)
        unwrapped_kwargs = ctx.unwrap_tensors(kwargs)

        with ctx.redispatch_to_next():
            out = run_with_rng_state(
                unwrapped_rng_state, op, *unwrapped_args, **unwrapped_kwargs
            )
            return ctx.wrap_tensors(out)

    return run_with_rng_state

