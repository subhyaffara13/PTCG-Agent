import functools
from typing import Callable

def preserve_global_state(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    """
    Context manager to:
        1) Save/restore torch.is_grad_enabled() state
        2) Save/restore torch random state
        3) Monkey patch torch.fx.graph_module._forward_from_src

    NOTE: Python random state is preserved in eval_frame_cpp.cpp instead,
    so that it wraps more of the compilation pipeline.
    """

    @functools.wraps(fn)
    def _fn(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        guards = GlobalStateGuard()
        prior_grad_mode = torch.is_grad_enabled()

        # Just in case we get left in a bad dispatch state we want to restore
        # it. This can happen because the dispatch bits aren't a true
        # stack/counter - so we can't just increment/decrement them as we enter
        # and leave.
        with (
            torch._C._PreserveDispatchKeyGuard(),
            maybe_disable_inference_mode(),
            maybe_disable_inference_mode_for_fake_prop(),
        ):
            prior_inference_mode = torch.is_inference_mode_enabled()
            prior_deterministic = torch.are_deterministic_algorithms_enabled()
            prior_warn_only = torch.is_deterministic_algorithms_warn_only_enabled()
            prior_mobile_allocator_state = (
                torch._C._is_default_mobile_cpu_allocator_set()
            )
            prior_dtype = torch.get_default_dtype()
            torch_rng_state = torch.random.get_rng_state()
            cuda_rng_state = None
            if torch.cuda.is_available():
                with torch._C.DisableTorchFunction():
                    cuda_rng_state = torch.cuda.get_rng_state()
            cuda_matmul_fp32_prec = torch._C._get_fp32_precision_getter(
                "cuda", "matmul"
            )
            prior_fwd_from_src = torch.fx.graph_module._forward_from_src
            torch.fx.graph_module._forward_from_src = fx_forward_from_src_skip_result
            cleanup = setup_compile_debug()
            exit_stack = contextlib.ExitStack()
            exit_stack.enter_context(
                torch.fx._symbolic_trace._maybe_revert_all_patches()
            )
            reset_user_object_tracking()
            try:
                return fn(*args, **kwargs)
            finally:
                cleanup.close()
                exit_stack.close()
                torch._C._set_grad_enabled(prior_grad_mode)
                torch.autograd.grad_mode._enter_inference_mode(prior_inference_mode)
                torch.use_deterministic_algorithms(
                    prior_deterministic, warn_only=prior_warn_only
                )
                torch.random.set_rng_state(torch_rng_state)
                torch.set_default_dtype(prior_dtype)
                curr_mobile_allocator_state = (
                    torch._C._is_default_mobile_cpu_allocator_set()
                )
                if prior_mobile_allocator_state != curr_mobile_allocator_state:
                    torch._C._unset_default_mobile_cpu_allocator()
                if cuda_rng_state is not None:
                    with torch._C.DisableTorchFunction():
                        torch.cuda.set_rng_state(cuda_rng_state)
                torch._C._set_fp32_precision_setter(
                    "cuda", "matmul", cuda_matmul_fp32_prec
                )
                torch.fx.graph_module._forward_from_src = prior_fwd_from_src
                assert guards.check(), (
                    f"Global {guards.reason()}state changed while dynamo tracing, please report a bug"
                )

    _fn._torchdynamo_orig_backend = fn  # type: ignore[attr-defined]
    return _fn

