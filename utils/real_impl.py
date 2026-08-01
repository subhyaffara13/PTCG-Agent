
def real_impl(
    gm: GraphModule,
    *args: Any,
    **kwargs: Any,
) -> tuple[torch.Tensor]:
    return gm(*args, **kwargs)


def real_impl(self: ComplexTensor) -> torch.Tensor:
    re, _ = split_complex_tensor(self)
    return re

