
def _remove_symbols_without_guarding(x: torch.Tensor, fallback: int) -> torch.Tensor:
    shape = list(x.shape)

    def realize_symbol(d: torch.SymInt | int) -> int:
        return optimization_hint(d, fallback=fallback)

    shape = [realize_symbol(s) for s in shape]
    stride = [realize_symbol(s) for s in x.stride()]
    return x.new_empty_strided(shape, stride=stride)

