
def meta_reflection_pad1d_backward(grad_output, input, padding):
    return _pad1d_backward_common(grad_output, input, padding, is_reflection=True)

