
def log_sigmoid_backward(grad_output: Tensor, self: Tensor, buffer: Tensor) -> Tensor:
    in_negative = self < 0
    max_deriv = torch.where(in_negative, 1, 0)
    sign = torch.where(in_negative, 1, -1)
    # On CPU, forward saves buffer = exp(-|x|); reuse it to match the native kernel.
    # On CUDA/XPU, buffer is empty so we recompute.
    z = buffer if buffer.numel() > 0 else torch.exp(-torch.abs(self))
    return grad_output * (max_deriv - sign * (z / (1 + z)))

