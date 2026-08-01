
def meta_adaptive_max_pool3d(input, output_size):
    ndim = input.ndim
    torch._check(
        ndim in (4, 5),
        lambda: f"adaptive_max_pool3d(): Expected 4D or 5D tensor, but got: {input.shape}",
    )
    for i in range(1, ndim):
        torch._check(
            input.size(i) > 0,
            lambda: (
                f"adaptive_max_pool3d(): Expected input to have non-zero size for non-batch dimensions, "
                f"but input has sizes {input.shape} with dimension {i} being empty"
            ),
        )

    torch._check(
        len(output_size) == 3,
        lambda: "adaptive_max_pool3d(): internal error: output_size.size() must be 3",
    )

    dimD = 0
    sizeB = 1
    sizeD = 0

    if ndim == 5:
        sizeB = input.size(0)
        dimD += 1

    sizeD = input.size(dimD)
    osizeT, osizeH, osizeW = output_size

    if ndim == 4:
        out_shape = (sizeD, osizeT, osizeH, osizeW)
    else:
        out_shape = (sizeB, sizeD, osizeT, osizeH, osizeW)  # type: ignore[assignment]

    out = input.new_empty(out_shape)
    indices = input.new_empty(out_shape, dtype=torch.int64)

    return out, indices

