
def eager_prepare_softmax(x: Tensor, dim: int) -> tuple[Tensor, Tensor]:
    amax = torch.amax(x, dim, keepdim=True)
    return amax, torch.sum(torch.exp(x - amax), dim, keepdim=True)

