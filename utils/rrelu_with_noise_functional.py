
def rrelu_with_noise_functional(
    self: torch.Tensor,
    noise: torch.Tensor,
    lower: float = 0.125,
    upper: float = 0.3333333333333333,
    training: bool = False,
    generator: torch.Generator | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    if training:
        not_positive = self <= 0
        r = aten.uniform(self, lower, upper, generator=generator)
        output = torch.where(not_positive, self * r, self)
        noise_out = torch.where(not_positive, r, 1)
        return output, noise_out
    else:
        negative_slope = (lower + upper) / 2
        return aten.leaky_relu(self, negative_slope), torch.Tensor()

