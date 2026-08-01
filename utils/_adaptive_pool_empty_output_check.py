
def _adaptive_pool_empty_output_check(grad_output: Tensor, arg_name: str):
    ndim = grad_output.ndim
    for i in range(1, ndim):
        torch._check(
            grad_output.size(i) > 0,
            lambda: (
                f"{arg_name}(): Expected grad_output to have non-zero size for non-batch dimensions, "
                f"but grad_output has sizes {grad_output.shape} with dimension {i} being empty"
            ),
        )

