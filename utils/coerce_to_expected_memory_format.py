
def coerce_to_expected_memory_format(
    x: torch.Tensor, memory_format: MemoryFormatMeta
) -> torch.Tensor:
    if memory_format.memory_format is not None:
        # Coerce to torch.memory_format
        if not x.is_contiguous(memory_format=memory_format.memory_format):
            x = x.contiguous(memory_format=memory_format.memory_format)
        return x

    expected_size = memory_format.size
    if expected_size is None:
        raise AssertionError("memory_format.size must not be None")
    expected_stride = memory_format.stride
    if expected_stride is None:
        raise AssertionError("memory_format.stride must not be None")
    # Expected size and stride are static ints
    # ok to use == to compare runtime tensor strides and shapes

    if x.shape == expected_size and x.stride() == expected_stride:
        # Runtime tangent size and stride are the same as expected, no need to coerce
        return x

    # Empty_strided creates a raw Tensor.
    # We are guaranteed that only raw Tensors has expected size and stride.
    # Subclasses have only expected memory_format.
    restrided = torch.empty_strided(
        size=expected_size,
        stride=expected_stride,
        dtype=x.dtype,
        device=x.device,
        layout=x.layout,
        requires_grad=x.requires_grad,
    )
    restrided.copy_(x)
    return restrided

