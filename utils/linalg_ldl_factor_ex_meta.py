
def linalg_ldl_factor_ex_meta(
    self: Tensor,
    *,
    hermitian: bool = False,
    check_errors: bool = False,
) -> tuple[Tensor, Tensor, Tensor]:
    squareCheckInputs(self, "torch.linalg.ldl_factor_ex")
    checkFloatingOrComplex(self, "torch.linalg.ldl_factor_ex")
    LD = torch.empty_strided(
        size=self.shape,
        stride=make_contiguous_strides_for(self.shape, row_major=False),
        dtype=self.dtype,
        device=self.device,
    )
    pivots = self.new_empty(self.shape[:-1], dtype=torch.int)
    info = self.new_empty(self.shape[:-2], dtype=torch.int)
    return LD, pivots, info

