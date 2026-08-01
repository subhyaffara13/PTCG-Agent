
def conv1d_output_length(module: "torch.nn.Conv1d", input_length: int) -> int:
    """
    Computes the output length of a 1D convolution layer according to torch's documentation:
    https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv1d.html
    """
    return int(
        (input_length + 2 * module.padding[0] - module.dilation[0] * (module.kernel_size[0] - 1) - 1)
        / module.stride[0]
        + 1
    )

