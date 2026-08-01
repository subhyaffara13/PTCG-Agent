
def upsample_nearest3d(input, output_size, scales_d=None, scales_h=None, scales_w=None):
    torch._check(
        input.numel() != 0 or multiply_integers(input.size()[1:]),
        lambda: f"Non-empty 5D data tensor expected but got a tensor with sizes {input.size()}",
    )
    full_output_size = upsample_common_check(
        input.size(), output_size, num_spatial_dims=3
    )
    return input.new_empty(full_output_size).to(
        memory_format=utils.suggest_memory_format(input)
    )


def upsample_nearest3d(
    input: Tensor,
    output_size: list[int],
    scales_d: float | None = None,
    scales_h: float | None = None,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales_d, scales_h, scales_w])


def upsample_nearest3d(
    x,
    output_size,
    scales_d: float | None = None,
    scales_h: float | None = None,
    scales_w: float | None = None,
):
    return upsample_nearestnd(x, output_size, (scales_d, scales_h, scales_w), n=3)

