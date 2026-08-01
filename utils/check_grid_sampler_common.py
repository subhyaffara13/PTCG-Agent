
def check_grid_sampler_common(input: Tensor, grid: Tensor):
    torch._check(
        input.device == grid.device,
        lambda: (
            f"grid_sampler(): expected input and grid to be on same device, but input "
            f"is on {input.device} and grid is on {grid.device}"
        ),
    )
    torch._check(
        input.layout == torch.strided and grid.layout == torch.strided,
        lambda: (
            f"grid_sampler(): expected input and grid to have torch.strided layout, but "
            f"input has {input.layout} and grid has {grid.layout}"
        ),
    )
    torch._check(
        input.shape[0] == grid.shape[0],
        lambda: (
            f"grid_sampler(): expected grid and input to have same batch size, but got "
            f"input with sizes {input.shape} and grid with sizes {grid.shape}"
        ),
    )
    torch._check(
        grid.shape[-1] == input.ndim - 2,
        lambda: (
            f"grid_sampler(): expected grid to have size {input.ndim - 2} in last "
            f"dimension, but got grid with sizes {grid.shape}"
        ),
    )

    for i in range(2, input.ndim):
        torch._check(
            input.shape[i] > 0,
            lambda: (
                f"grid_sampler(): expected input to have non-empty spatial dimensions, "
                f"but input has sizes {input.shape} with dimension {i} being empty"
            ),
        )

