
def _xor_sum_aten(
    inp: TensorLikeType,
    dims: DimsSequenceType | None,
    *,
    dtype: torch.dtype | None = None,
) -> Tensor:
    raise NotImplementedError("xor_sum only implemented with inductor")

