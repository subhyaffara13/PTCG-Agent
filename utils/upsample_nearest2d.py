from typing import Optional

def upsample_nearest2d(input, output_size, scales_h=None, scales_w=None):
    torch._check(
        input.numel() != 0 or multiply_integers(input.size()[1:]),
        lambda: f"Non-empty 4D data tensor expected but got a tensor with sizes {input.size()}",
    )
    full_output_size = upsample_common_check(
        input.size(), output_size, num_spatial_dims=2
    )
    output = input.new_empty(full_output_size)

    # convert output to correct memory format, if necessary
    memory_format = utils.suggest_memory_format(input)

    # following "heuristic: only use channels_last path when it's faster than the contiguous path"
    _, n_channels, _, _ = input.shape
    if input.device.type == "cuda" and n_channels < 4:
        memory_format = torch.contiguous_format

    output = output.contiguous(memory_format=memory_format)

    return output


def upsample_nearest2d(
    input: list[int],
    output_size: Optional[list[int]],
    scale_factors: Optional[list[float]],
):
    out: list[int] = []
    out.append(input[0])
    out.append(input[1])

    if scale_factors is None and output_size is None:
        raise AssertionError("Either output_size or scale_factors must be presented")

    if output_size is not None:
        if scale_factors is not None:
            raise AssertionError(
                "Must specify exactly one of output_size and scale_factors"
            )
        if len(output_size) != 2:
            raise AssertionError(
                f"Expected output_size to have length 2, but got {len(output_size)}"
            )
        out.append(output_size[0])
        out.append(output_size[1])

    if scale_factors is not None:
        if output_size is not None:
            raise AssertionError(
                "Must specify exactly one of output_size and scale_factors"
            )
        if len(scale_factors) != 2:
            raise AssertionError(
                f"Expected scale_factors to have length 2, but got {len(scale_factors)}"
            )
        out.append(int(input[2] * scale_factors[0]))
        out.append(int(input[3] * scale_factors[1]))

    return out


def upsample_nearest2d(
    input: Tensor,
    output_size: list[int],
    scales_h: float | None = None,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales_h, scales_w])


def upsample_nearest2d(
    x, output_size, scales_h: float | None = None, scales_w: float | None = None
):
    return upsample_nearestnd(x, output_size, (scales_h, scales_w), n=2)

