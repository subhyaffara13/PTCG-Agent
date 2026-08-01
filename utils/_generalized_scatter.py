
def _generalized_scatter(
    inp: torch.Tensor, src: torch.Tensor, view_ops: list[ViewOp]
) -> torch.Tensor:
    out = inp.clone()
    return _inplace_generalized_scatter(out, src, view_ops)

