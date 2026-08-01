
def custom_triton_ops_decomposition_disabled():
    return not torch._functorch.config.decompose_custom_triton_ops

