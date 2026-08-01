
def softmax_backward_data(parent, grad_output, output):
    """
    A function that calls the internal `_softmax_backward_data` PyTorch method and that adjusts the arguments according
    to the torch version detected.
    """

    from torch import _softmax_backward_data

    return _softmax_backward_data(grad_output, output, parent.dim, output.dtype)

