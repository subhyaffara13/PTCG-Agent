
def _safe_clone(src: torch.Tensor) -> torch.Tensor | None:
    if type(src) is not torch.Tensor:
        return None
    return src.clone()

