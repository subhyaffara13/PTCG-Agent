
def meta_bernoulli_p(self, p=0.5, generator=None):
    # https://github.com/pytorch/pytorch/issues/88612
    return torch.empty_like(self, memory_format=torch.contiguous_format)

