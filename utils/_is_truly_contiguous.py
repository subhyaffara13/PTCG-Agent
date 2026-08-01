
def _is_truly_contiguous(x: Tensor) -> bool:
    # Special case: Pytorch thinks that 1x1 channels_last convolution weights are
    # both contiguous and channels_last contiguous at the same time.
    # CuDNN does not agree though and refuses to select faster kernels.
    # It is the reason of having the extra check here.
    return x.stride(-1) == 1 and x.is_contiguous()

