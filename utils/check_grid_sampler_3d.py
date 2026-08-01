
def check_grid_sampler_3d(input: Tensor, grid: Tensor, interpolation_mode: int):
    torch._check(
        input.ndim == 5 and input.ndim == grid.ndim,
        lambda: (
            f"grid_sampler(): expected 5D input and grid with same number of "
            f"dimensions, but got input with sizes {input.shape}"
            f" and grid with sizes {grid.shape}"
        ),
    )
    torch._check(
        not (
            input.ndim == 5
            and interpolation_mode == GridSamplerInterpolation.BICUBIC.value
        ),
        lambda: "grid_sampler(): bicubic interpolation only supports 4D input",
    )

