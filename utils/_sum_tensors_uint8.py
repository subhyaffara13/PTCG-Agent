
def _sum_tensors_uint8(
    src: Iterable[Tensor], weights: Iterable[Tensor], weights_precision: Tensor
) -> Tensor:
    output = _sum_tensors(
        s.to(torch.int32) * c.to(torch.int32) for s, c in zip(src, weights)
    ) + (1 << (weights_precision - 1))
    output = output >> weights_precision
    return torch.clamp(output, 0, 255).to(torch.uint8)

