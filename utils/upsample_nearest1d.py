
def upsample_nearest1d(input, output_size, scales=None):
    torch._check(
        input.numel() != 0 or multiply_integers(input.size()[1:]),
        lambda: f"Non-empty 3D data tensor expected but got a tensor with sizes {input.size()}",
    )
    full_output_size = upsample_common_check(
        input.size(), output_size, num_spatial_dims=1
    )
    return input.new_empty(full_output_size).to(
        memory_format=utils.suggest_memory_format(input)
    )


def upsample_nearest1d(
    input: Tensor,
    output_size: list[int],
    scales: float | None = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales])


def upsample_nearest1d(x, output_size, scales: float | None = None):
    return upsample_nearestnd(x, output_size, (scales,), n=1)

