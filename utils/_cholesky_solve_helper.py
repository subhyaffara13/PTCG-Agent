
def _cholesky_solve_helper(self: Tensor, A: Tensor, upper: bool) -> Tensor:
    return cloneBatchedColumnMajor(self)

