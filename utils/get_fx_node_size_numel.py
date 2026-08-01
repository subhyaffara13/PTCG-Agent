
def get_fx_node_size_numel(size: torch.Size, fallback: int = 4096 * 4096) -> int:
    numel = functools.reduce(operator.mul, size, 1)
    result = optimization_hint(numel, fallback=fallback)
    return result

