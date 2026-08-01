
def grid_sampler_2d_backward_meta(
    grad_output,
    input,
    grid,
    interpolation_mode,
    padding_mode,
    align_corners,
    output_mask,
):
    input_requires_grad = output_mask[0]
    if input_requires_grad:
        grad_input = torch.zeros_like(input, memory_format=torch.contiguous_format)
    else:
        grad_input = None
    grad_grid = torch.empty_like(grid, memory_format=torch.contiguous_format)
    return (grad_input, grad_grid)

