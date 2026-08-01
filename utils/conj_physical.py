
def conj_physical(self: torch.Tensor) -> torch.Tensor:
    if self.is_complex():
        return NotImplemented
    return self


def conj_physical(input: TensorLikeType):
    if not utils.is_complex_dtype(input.dtype):
        return input
    return prims.conj_physical(input)

