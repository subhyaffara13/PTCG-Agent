
def get_global_state_key() -> GlobalStateKey:
    return (
        torch.is_grad_enabled(),
        torch.is_inference_mode_enabled(),
        torch.get_num_threads(),
        torch._C._get_cublas_allow_fp16_reduced_precision_reduction(),
        torch._C._get_cublas_allow_bf16_reduced_precision_reduction(),
        torch.get_default_dtype(),
        torch.are_deterministic_algorithms_enabled(),
        torch._C._get_cublas_allow_tf32(),
        torch.is_deterministic_algorithms_warn_only_enabled(),
        torch._C._autograd._saved_tensors_hooks_is_enabled(),  # type: ignore[attr-defined]
    )

