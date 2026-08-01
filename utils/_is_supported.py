
def _is_supported(input_size, kernel_size, stride, padding, dilation):
    if dilation[-1] != 1:
        raise RuntimeError("Dilation must be 1 for tensor parallel convolution.")
    if padding[-1] != 0:
        if stride[-1] != 1:
            raise RuntimeError(
                "Stride must be 1 when there is padding for tensor parallel convolution."
            )
        if kernel_size[-1] // 2 > input_size[-1]:
            raise RuntimeError(
                "kernel_size[-1] // 2 should be less than or equal to input_size[-1] for tensor parallel convolution."
            )
    else:
        if not (input_size[-1] % stride[-1] == 0 and stride[-1] == kernel_size[-1]):
            raise RuntimeError(
                "It requires that input_size[-1] is divisible by stride[-1] and stride[-1] equals kernel_size[-1] "
                "when there is padding for tensor parallel convolution."
            )
    return True

