
def pooling_output_shape(inputSize, kernelSize, pad, stride, dilation, ceil_mode):
    torch._check(stride != 0, lambda: "stride should not be zero")
    torch._check(pad >= 0, lambda: f"pad must be non-negative, but got pad: {pad}")
    torch._check(
        pad <= ((kernelSize - 1) * dilation + 1) // 2,
        lambda: (
            f"pad should be at most half of effective kernel size, but got pad={pad}, "
            f"kernel_size={kernelSize} and dilation={dilation}"
        ),
    )
    return pooling_output_shape_pad_lr(
        inputSize, kernelSize, pad, pad, stride, dilation, ceil_mode
    )


def pooling_output_shape(
    inputSize: int,
    kernelSize: int,
    pad_l: int,
    stride: int,
    dilation: int,
    ceil_mode: bool,
):
    if stride == 0:
        raise AssertionError("stride should not be zero")
    return pooling_output_shape_pad_lr(
        inputSize, kernelSize, pad_l, pad_l, stride, dilation, ceil_mode
    )

