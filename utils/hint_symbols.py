
def hint_symbols(
    ds: Sequence[int | torch.SymInt],
) -> list[int]:
    """Helper to convert symbolic dimensions to their concrete hint values."""
    from torch.fx.experimental.symbolic_shapes import optimization_hint

    return [optimization_hint(d) for d in ds]

