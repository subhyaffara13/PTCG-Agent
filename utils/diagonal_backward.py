
def diagonal_backward(
    grad_output: Tensor, input_sizes: list[int], offset: int, dim1: int, dim2: int
):
    grad_input = grad_output.new_zeros(input_sizes)
    return torch.diagonal_scatter(grad_input, grad_output, offset, dim1, dim2)


def diagonal_backward(
    grad_output: torch.Tensor, input_sizes: list[int], offset: int, dim1: int, dim2: int
) -> torch.Tensor:
    grad_input = grad_output.new_zeros(input_sizes)
    return torch.diagonal_scatter(grad_input, grad_output, offset, dim1, dim2)

