
def _is_fake_tensor(t: object) -> TypeIs[FakeTensor]:
    from torch._subclasses.fake_tensor import FakeTensor

    return isinstance(t, FakeTensor)


def _is_fake_tensor(t: torch.Tensor) -> TypeIs[FakeTensor]:
    return isinstance(t, FakeTensor)

