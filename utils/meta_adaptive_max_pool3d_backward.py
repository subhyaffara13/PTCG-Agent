
def meta_adaptive_max_pool3d_backward(grad_output, input, indices):
    _adaptive_pool_empty_output_check(grad_output, "adaptive_max_pool3d_backward")
    return input.new_empty(input.shape)

