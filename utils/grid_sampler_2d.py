
def grid_sampler_2d(
    a: Tensor,
    grid: Tensor,
    interpolation_mode: int = 0,
    padding_mode: int = 0,
    align_corners: bool = False,
) -> Tensor:
    return _grid_sampler_2d(
        a,
        grid=grid,
        interpolation_mode=interpolation_mode,
        padding_mode=padding_mode,
        align_corners=align_corners,
    )


def grid_sampler_2d(
    a: torch.Tensor,
    grid: torch.Tensor,
    interpolation_mode: int = 0,
    padding_mode: int = 0,
    align_corners: bool = False,
) -> torch.Tensor:
    # We do not expand the grid (_expand_grid=False) on cpu for performance reasons
    # Experimenting locally it was found that compiled CUDA code is accelerated by ~5x
    # and CPU code by ~2x on bicubic mode, if we expand the grid from (N, H, W, 2) into (N, C, H, W, 2)
    # However, this leads to a slowdown around ~0.8x on CPU bilinear mode, channels first.
    # Thus we apply this hack to not expand the grid for this case.
    _expand_grid = not (
        a.device == torch.device("cpu")
        and interpolation_mode == 0
        and a.is_contiguous(memory_format=torch.contiguous_format)
    )

    output = decomp_grid_sampler_2d(
        a,
        grid=grid,
        interpolation_mode=interpolation_mode,
        padding_mode=padding_mode,
        align_corners=align_corners,
        _expand_grid=_expand_grid,
    )
    return output

