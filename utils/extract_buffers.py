
def extract_buffers(
    mod: nn.Module,
) -> tuple[tuple[Tensor, ...], tuple[str, ...], dict[str, list[str]]]:
    return _extract_members(mod, mod.named_buffers, lambda x: x)

