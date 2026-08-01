
def bernoulli_(self, p=0.5):
    if self.device == torch.device("cpu"):
        return NotImplemented
    return self.copy_(torch.rand_like(self, dtype=torch.float32) < p)


def bernoulli_(x, *args):
    assert config.fallback_random or x.get_device() == torch.device("cpu"), (
        "this should be handled in decomps unless config.fallback_random or the device is CPU"
    )
    x.realize()
    op_overload = (
        aten.bernoulli_.float
        if len(args) == 0 or isinstance(args[0], float)
        else aten.bernoulli_.Tensor
    )
    ir.InplaceBernoulliFallback(op_overload, x, *args)
    return x

