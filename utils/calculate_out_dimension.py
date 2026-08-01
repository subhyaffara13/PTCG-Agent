
def calculate_out_dimension(d_in, module_instance, index):
    """
    For calculating h_in and w_out according to the conv2D documentation
    """
    padding = (
        (module_instance.padding, module_instance.padding)
        if isinstance(module_instance.padding, int)
        else module_instance.padding
    )
    kernel_size = (
        (module_instance.kernel_size, module_instance.kernel_size)
        if isinstance(module_instance.kernel_size, int)
        else module_instance.kernel_size
    )
    stride = (
        (module_instance.stride, module_instance.stride)
        if isinstance(module_instance.stride, int)
        else module_instance.stride
    )
    dilation = (
        (module_instance.dilation, module_instance.dilation)
        if isinstance(module_instance.dilation, int)
        else module_instance.dilation
    )

    DIMENSION_TYPES = (int, sympy.Symbol)

    if d_in == Dyn:
        return Dyn

    elif isinstance(d_in, DIMENSION_TYPES):
        n = d_in + 2 * padding[index] - dilation[index] * (kernel_size[index] - 1) - 1

        return (n // stride[0]) + 1

    else:
        raise TypeError(
            f"{d_in} in {module_instance} must be a number or Dyn. Received {type(d_in)}"
        )

