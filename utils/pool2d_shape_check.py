
def pool2d_shape_check(
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
):
    ndim = input.dim()
    nOutputPlane = nInputPlane

    torch._check(
        kW > 0 and kH > 0,
        lambda: f"kernel size should be greater than zero, but got kH: {kH}, kW: {kW}",
    )
    torch._check(
        dW > 0 and dH > 0,
        lambda: f"stride should be greater than zero, but got dH: {dH}, dW: {dW}",
    )
    torch._check(
        dilationH > 0 and dilationW > 0,
        lambda: f"dilation should be greater than zero, but got dilationH: {dilationH}, dilationW: {dilationW}",
    )

    valid_dims = input.size(1) != 0 and input.size(2) != 0

    if memory_format == torch.channels_last:
        torch._check(
            ndim == 4 and valid_dims and input.size(3) != 0,
            lambda: "Expected 4D (batch mode) tensor expected for input with channels_last layout"
            f" with optional 0 dim batch size for input, but got: {input.size()}",
        )
    else:
        torch._check(
            (ndim == 3 and input.size(0) != 0 and valid_dims)
            or (ndim == 4 and valid_dims and input.size(3) != 0),
            lambda: f"Expected 3D or 4D (batch mode) tensor with optional 0 dim batch size for input, but got: {input.size()}",
        )

    torch._check(
        kW // 2 >= padW and kH // 2 >= padH,
        lambda: "pad should be smaller than or equal to half of kernel size, but got "
        f"padW = {padW}, padH = {padH}, kW = {kW}, kH = {kH}",
    )

    torch._check(
        outputWidth >= 1 and outputHeight >= 1,
        lambda: f"Given input size: ({nInputPlane}x{inputHeight}x{inputWidth}). "
        f"Calculated output size: ({nOutputPlane}x{outputHeight}x{outputWidth}). "
        "Output size is too small",
    )


def pool2d_shape_check(
    input: list[int],
    kH: int,
    kW: int,
    dH: int,
    dW: int,
    padH: int,
    padW: int,
    dilationH: int,
    dilationW: int,
    nInputPlane: int,
    inputHeight: int,
    inputWidth: int,
    outputHeight: int,
    outputWidth: int,
):
    ndim = len(input)

    if not (kW > 0 and kH > 0):
        raise AssertionError(f"Expected kW ({kW}) > 0 and kH ({kH}) > 0")
    if not (dW > 0 and dH > 0):
        raise AssertionError(f"Expected dW ({dW}) > 0 and dH ({dH}) > 0")
    if not (dilationH > 0 and dilationW > 0):
        raise AssertionError(
            f"Expected dilationH ({dilationH}) > 0 and dilationW ({dilationW}) > 0"
        )

    valid_dims = input[1] != 0 and input[2] != 0
    if not (
        ndim == 3
        and input[0] != 0
        and valid_dims
        or (ndim == 4 and valid_dims and input[3] != 0)
    ):
        raise AssertionError(f"Invalid input dimensions: ndim={ndim}, input={input}")

    if not (kW // 2 >= padW and kH // 2 >= padH):
        raise AssertionError(
            f"Expected kW//2 ({kW // 2}) >= padW ({padW}) and "
            f"kH//2 ({kH // 2}) >= padH ({padH})"
        )
    if not (outputWidth >= 1 and outputHeight >= 1):
        raise AssertionError(
            f"Expected outputWidth ({outputWidth}) >= 1 and "
            f"outputHeight ({outputHeight}) >= 1"
        )

