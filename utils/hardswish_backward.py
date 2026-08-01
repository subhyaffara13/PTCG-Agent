
def hardswish_backward(grad_output: Tensor, self: Tensor) -> Tensor:
    return torch.where(
        self <= -3,
        0.0,
        torch.where(self < 3, grad_output * ((self / 3) + 0.5), grad_output),
    )

