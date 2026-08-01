
def meta_bernoulli(self, *, generator=None):
    # https://github.com/pytorch/pytorch/issues/88612
    return torch.empty_like(self, memory_format=torch.contiguous_format)

