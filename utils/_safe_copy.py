
def _safe_copy(dst: torch.Tensor, src: torch.Tensor | None) -> None:
    if type(src) is not torch.Tensor:
        return
    dst.copy_(src)

