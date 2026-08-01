
def register_run_and_save_rng_state_op():
    class RunAndSaveRngState(HigherOrderOperator):
        def __init__(self):
            super().__init__("run_and_save_rng_state", cacheable=True)

        def __call__(self, op, *args, **kwargs):
            # pyrefly: ignore [missing-attribute]
            return super().__call__(op, *args, **kwargs)

    run_and_save_rng_state = RunAndSaveRngState()

    run_and_save_rng_state.py_impl(DispatchKey.Autograd)(
        autograd_not_implemented(run_and_save_rng_state, deferred_error=True)
    )

    @run_and_save_rng_state.py_impl(DispatchKey.CUDA)
    def impl_cuda(op, *args, **kwargs):
        return torch.cuda.get_rng_state(), op(*args, **kwargs)

    @run_and_save_rng_state.py_impl(DispatchKey.CPU)
    def impl_cpu(op, *args, **kwargs):
        return torch.get_rng_state(), op(*args, **kwargs)

    @run_and_save_rng_state.py_impl(DispatchKey.HPU)
    def impl_hpu(op, *args, **kwargs):
        if hasattr(torch, "hpu"):
            return torch.hpu.get_rng_state(), op(*args, **kwargs)
        raise RuntimeError("functionalize a hpu RNG operator is not supported.")

    @run_and_save_rng_state.py_impl(DispatchKey.XPU)
    def impl_xpu(op, *args, **kwargs):
        return torch.xpu.get_rng_state(), op(*args, **kwargs)

    @run_and_save_rng_state.py_impl(DispatchKey.BackendSelect)
    def impl_backend_select(op, *args, **kwargs):
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
        return impl(op, *args, **kwargs)

    @run_and_save_rng_state.py_impl(FakeTensorMode)
    def impl_fake_tensor_mode(mode, op, *args, **kwargs):
        # Check device to call the right impl
        with mode:
            return impl_backend_select(op, *args, **kwargs)

    @run_and_save_rng_state.py_impl(ProxyTorchDispatchMode)
    def impl_proxy_dispatch_mode(mode, op, *args, **kwargs):
        out = impl_backend_select(op, *args, **kwargs)
        proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, (op, *args))
        proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)
        out_proxy = mode.tracer.create_proxy(
            "call_function", run_and_save_rng_state, proxy_args, proxy_kwargs
        )
        return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)

    return run_and_save_rng_state

