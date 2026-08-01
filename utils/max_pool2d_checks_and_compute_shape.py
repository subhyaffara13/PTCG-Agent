
def max_pool2d_checks_and_compute_shape(
    input,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode,
):
    # Reference: aten/src/ATen/native/DilatedMaxPool2d.cpp
    def unpack(name, val):
        torch._check(
            len(val) in [1, 2],
            lambda: f"max_pool2d: {name} must either be a single int, or a tuple of two ints",
        )
        H = val[0]
        W = H if len(val) == 1 else val[1]
        return H, W

    kH, kW = unpack("kernel_size", kernel_size)

    torch._check(
        len(stride) in [0, 1, 2],
        lambda: "max_pool2d: stride must either be omitted, a single int, or a tuple of two ints",
    )
    if len(stride) == 0:
        dH, dW = kH, kW
    else:
        dH, dW = unpack("stride", stride)

    padH, padW = unpack("padding", padding)
    dilationH, dilationW = unpack("dilation", dilation)
    nInputPlane = input.size(-3)
    inputHeight = input.size(-2)
    inputWidth = input.size(-1)

    memory_format = utils.suggest_memory_format(input)
    if memory_format == torch.channels_last:
        torch._check(
            input.dim() == 4,
            lambda: "non-empty 4D (batch mode) tensor expected for input with channels_last layout",
        )
    elif memory_format == torch.contiguous_format:
        torch._check(
            input.dim() in [3, 4],
            lambda: "non-empty 3D or 4D (batch mode) tensor expected for input",
        )
    else:
        torch._check(
            False,
            lambda: "Unsupported memory format. Supports only ChannelsLast, Contiguous",
        )

    outputHeight = pooling_output_shape(inputHeight, kH, padH, dH, dilationH, ceil_mode)
    outputWidth = pooling_output_shape(inputWidth, kW, padW, dW, dilationW, ceil_mode)

    pool2d_shape_check(
        input,
        kH,
        kW,
        dH,
        dW,
        padH,
        padW,
        dilationH,
        dilationW,
        nInputPlane,
        inputHeight,
        inputWidth,
        outputHeight,
        outputWidth,
        memory_format,
    )

    return nInputPlane, outputHeight, outputWidth

