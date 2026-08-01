
def glu_backward(grad_output: Tensor, self: Tensor, dim: int) -> Tensor:
    if self.dim() <= 0:
        raise AssertionError("glu does not support 0-dimensional tensors")
    wrap_dim = utils.canonicalize_dim(self.dim(), dim)
    nIn = self.size(wrap_dim)
    if nIn % 2 != 0:
        raise AssertionError(
            f"Halving dimension must be even, but dimension {wrap_dim} is size {nIn}"
        )
    inputSize = nIn // 2
    firstHalf = self.narrow(wrap_dim, 0, inputSize)
    secondHalf = self.narrow(wrap_dim, inputSize, inputSize)
    gradInputFirstHalf = torch.sigmoid(secondHalf)
    gradInputSecondHalf = (
        (1.0 - gradInputFirstHalf) * gradInputFirstHalf * firstHalf * grad_output
    )
    gradInputFirstHalf = gradInputFirstHalf * grad_output
    return torch.cat([gradInputFirstHalf, gradInputSecondHalf], dim=wrap_dim)

