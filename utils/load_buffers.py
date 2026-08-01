
def load_buffers(
    mod: nn.Module,
    names: Sequence[str],
    buffers: Sequence[Tensor],
    as_params: bool = False,
) -> None:
    accessor = NamedMemberAccessor(mod)
    accessor.set_tensors(names, buffers)

