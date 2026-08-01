
def get_padding_value(padding=None, kernel_size=7, stride=1, dilation=1) -> tuple[tuple, bool]:
    r"""
    Utility function to get the tuple padding value given the kernel_size and padding.

    Args:
        padding (Union[`str`, `int`], *optional*):
            Padding value, can be either `"same"`, `"valid"`. If a different value is provided the default padding from
            PyTorch is used.
        kernel_size (`int`, *optional*, defaults to 7):
            Kernel size of the convolution layers.
        stride (`int`, *optional*, defaults to 1):
            Stride value of the convolution layers.
        dilation (`int`, *optional*, defaults to 1):
            Dilation value of the convolution layers.
    """
    dynamic = False
    if padding is None:
        padding = ((stride - 1) + dilation * (kernel_size - 1)) // 2
        return padding, dynamic

    if isinstance(padding, str):
        # for any string padding, the padding will be calculated for you, one of three ways
        padding = padding.lower()
        if padding == "same":
            # TF compatible 'SAME' padding, has a performance and GPU memory allocation impact
            if stride == 1 and (dilation * (kernel_size - 1)) % 2 == 0:
                # static case, no extra overhead
                padding = ((stride - 1) + dilation * (kernel_size - 1)) // 2
            else:
                # dynamic 'SAME' padding, has runtime/GPU memory overhead
                padding = 0
                dynamic = True
        elif padding == "valid":
            # 'VALID' padding, same as padding=0
            padding = 0
        else:
            # Default to PyTorch style 'same'-ish symmetric padding
            padding = ((stride - 1) + dilation * (kernel_size - 1)) // 2
    return padding, dynamic

