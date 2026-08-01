
def layout_or_default(layout: torch.layout | None) -> torch.layout:
    return layout if layout is not None else torch.strided

