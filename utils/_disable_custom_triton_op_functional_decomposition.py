
def _disable_custom_triton_op_functional_decomposition():
    old = torch._functorch.config.decompose_custom_triton_ops
    try:
        # pyrefly: ignore [bad-assignment]
        torch._functorch.config.decompose_custom_triton_ops = False
        yield torch._functorch.config.decompose_custom_triton_ops
    finally:
        torch._functorch.config.decompose_custom_triton_ops = old

