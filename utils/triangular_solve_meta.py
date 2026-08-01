
def triangular_solve_meta(
    self: Tensor,
    A: Tensor,
    upper: bool = True,
    transpose: bool = False,
    unitriangular: bool = False,
) -> tuple[Tensor, Tensor]:
    torch._check(
        self.ndim >= 2,
        lambda: (
            f"torch.triangular_solve: Expected b to have at least 2 dimensions, "
            f"but it has {self.ndim} dimensions instead"
        ),
    )
    torch._check(
        A.ndim >= 2,
        lambda: (
            f"torch.triangular_solve: Expected A to have at least 2 dimensions, "
            f"but it has {A.ndim} dimensions instead"
        ),
    )

    linearSolveCheckInputs(self, A, "triangular_solve")

    if A.layout == torch.strided:
        self_broadcast_size, A_broadcast_size = _linalg_broadcast_batch_dims(self, A)
        solution = torch.empty_strided(
            size=self_broadcast_size,
            stride=make_contiguous_strides_for(self_broadcast_size, row_major=False),
            dtype=self.dtype,
            device=self.device,
        )
        cloned_coefficient = torch.empty_strided(
            size=A_broadcast_size,
            stride=make_contiguous_strides_for(A_broadcast_size, row_major=False),
            dtype=A.dtype,
            device=A.device,
        )
    elif A.layout == torch.sparse_csr or A.layout == torch.sparse_bsr:
        solution = torch.empty_like(self)
        cloned_coefficient = self.new_empty([0])
    else:
        torch._check(False, lambda: "triangular_solve: Got an unexpected layout.")
    return solution, cloned_coefficient  # type: ignore[possibly-undefined]

