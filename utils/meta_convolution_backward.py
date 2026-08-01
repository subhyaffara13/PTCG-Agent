
def meta_convolution_backward(
    grad_output_,
    input_,
    weight_,
    bias_sizes_opt,
    stride,
    padding,
    dilation,
    transposed,
    output_padding,
    groups,
    output_mask,
):
    # High level logic taken from slow_conv3d_backward_cpu which should
    # be representative of all convolution_backward impls
    backend_grad_input = None
    backend_grad_weight = None
    backend_grad_bias = None

    # All GPU backends compute output memory format via
    # determine_backend_memory_format(input, weight, backend) — which calls
    # cudnn_conv_suggest_memory_format(input, weight), mps_conv_use_channels_last(input, weight),
    # etc. The format depends only on input and weight, NOT on grad_output.
    # Both grad_input and grad_weight use this same backend_memory_format.
    # See: https://github.com/pytorch/pytorch/issues/171622
    def _conv_memory_format(t1, t2):
        fmt1 = suggest_memory_format(t1)
        fmt2 = suggest_memory_format(t2)
        if fmt1 == torch.channels_last or fmt2 == torch.channels_last:
            return torch.channels_last
        if fmt1 == torch.channels_last_3d or fmt2 == torch.channels_last_3d:
            return torch.channels_last_3d
        return torch.contiguous_format

    memory_format = _conv_memory_format(input_, weight_)
    if output_mask[0]:
        backend_grad_input = grad_output_.new_empty(input_.size()).to(
            memory_format=memory_format
        )
    if output_mask[1]:
        backend_grad_weight = grad_output_.new_empty(weight_.size()).to(
            memory_format=memory_format
        )
    if output_mask[2]:
        backend_grad_bias = grad_output_.new_empty(bias_sizes_opt)

    return (backend_grad_input, backend_grad_weight, backend_grad_bias)

