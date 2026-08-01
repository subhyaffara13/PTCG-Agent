
def meta_rrelu_with_noise_functional(
    self, noise, lower=0.125, upper=0.3333333333333333, training=False, generator=None
):
    return torch.empty_like(self), torch.empty_like(noise)

