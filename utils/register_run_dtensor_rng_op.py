
def register_run_dtensor_rng_op():
    """
    Register a higher-order operator for DTensor distributed random operations.
    Takes pre-computed integer offsets (start_offset_incr, end_offset_incr), an op,
    and args. Internally adjusts the RNG state using the offsets before/after
    running the op.

    The offsets are computed at trace time from the DTensorSpec, so the compiled graph
    contains only plain integers — no DTensorSpec or DeviceMesh objects.
    """

    class RunDTensorRngOp(HigherOrderOperator):
        def __init__(self):
            super().__init__("run_dtensor_rng_op", cacheable=True)

        def __call__(self, start_offset_incr, end_offset_incr, op, *args, **kwargs):
            # pyrefly: ignore [missing-attribute]
            return super().__call__(
                start_offset_incr, end_offset_incr, op, *args, **kwargs
            )

    run_dtensor_rng_op = RunDTensorRngOp()

    run_dtensor_rng_op.py_impl(DispatchKey.Autograd)(
        autograd_not_implemented(run_dtensor_rng_op, deferred_error=True)
    )

    @run_dtensor_rng_op.py_impl(DispatchKey.CUDA)
    def impl_cuda(start_offset_incr, end_offset_incr, op, *args, **kwargs):
        from torch.distributed.tensor._random import _PhiloxState

        state = _PhiloxState(torch.cuda.get_rng_state())
        old_offset = state.offset.clone()
        state.offset = old_offset + start_offset_incr

        device = (
            args[0].device
            if args and hasattr(args[0], "device")
            else torch.device(f"cuda:{torch.cuda.current_device()}")
        )
        with torch.random.fork_rng(devices=[device], device_type="cuda"):
            torch.cuda.set_rng_state(state.state)
            try:
                out = op(*args, **kwargs)
            finally:
                state.offset = old_offset + end_offset_incr

        torch.cuda.set_rng_state(state.state)
        return out

    @run_dtensor_rng_op.py_impl(DispatchKey.BackendSelect)
    def impl_backend_select(start_offset_incr, end_offset_incr, op, *args, **kwargs):
        device = get_device(args, kwargs)
        if device != "cuda":
            raise RuntimeError(
                f"run_dtensor_rng_op only supports CUDA device, got {device}. "
                f"This operator is designed for distributed random operations on CUDA."
            )
        return impl_cuda(start_offset_incr, end_offset_incr, op, *args, **kwargs)

    @run_dtensor_rng_op.py_impl(FakeTensorMode)
    def impl_fake_tensor_mode(
        mode, start_offset_incr, end_offset_incr, op, *args, **kwargs
    ):
        with mode:
            return op(*args, **kwargs)

    @run_dtensor_rng_op.py_impl(ProxyTorchDispatchMode)
    def impl_proxy_dispatch_mode(
        mode, start_offset_incr, end_offset_incr, op, *args, **kwargs
    ):
        with disable_proxy_modes_tracing():
            out = run_dtensor_rng_op(
                start_offset_incr, end_offset_incr, op, *args, **kwargs
            )
        proxy_args = pytree.tree_map(
            mode.tracer.unwrap_proxy, (start_offset_incr, end_offset_incr, op, *args)
        )
        proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)
        out_proxy = mode.tracer.create_proxy(
            "call_function", run_dtensor_rng_op, proxy_args, proxy_kwargs
        )
        return track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)

    @run_dtensor_rng_op.py_functionalize_impl
    def impl_functional(ctx, start_offset_incr, end_offset_incr, op, *args, **kwargs):
        unwrapped_args = ctx.unwrap_tensors(args)
        unwrapped_kwargs = ctx.unwrap_tensors(kwargs)

        with ctx.redispatch_to_next():
            out = run_dtensor_rng_op(
                start_offset_incr,
                end_offset_incr,
                op,
                *unwrapped_args,
                **unwrapped_kwargs,
            )
            return ctx.wrap_tensors(out)

    return run_dtensor_rng_op

