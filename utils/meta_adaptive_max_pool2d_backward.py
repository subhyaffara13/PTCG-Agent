
def meta_adaptive_max_pool2d_backward(grad_output, input, indices):
    ndim = grad_output.ndim
    torch._check(
        ndim in (3, 4),
        lambda: f"adaptive_max_pooling2d_backward(): Expected 3D or 4D grad_output, but got: {grad_output.shape}",
    )

    _adaptive_pool_empty_output_check(grad_output, "adaptive_max_pool2d_backward")

    torch._check(
        input.dtype == grad_output.dtype,
        lambda: f"expected dtype {input.dtype} for `grad_output` but got dtype {grad_output.dtype}",
    )

    memory_format = utils.suggest_memory_format(input)
    return input.new_empty(input.shape).to(memory_format=memory_format)

