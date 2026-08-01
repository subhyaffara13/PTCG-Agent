
def bernoulli_p(self, p=0.5, *, generator=None):
    if self.device == torch.device("cpu"):
        return NotImplemented
    if generator is not None:
        raise AssertionError(f"generator must be None, got {generator}")
    return torch.rand_like(self, dtype=torch.float32) < p


def bernoulli_p(x, *args):
    assert config.fallback_random or x.get_device() == torch.device("cpu"), (
        "this should be handled in decomps unless config.fallback_random or the device is CPU"
    )
    return bernoulli_(clone(x), *args)

