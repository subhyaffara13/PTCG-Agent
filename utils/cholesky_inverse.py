
def cholesky_inverse(self: Tensor, upper: bool = False) -> Tensor:
    squareCheckInputs(self, "cholesky_inverse")
    return cloneBatchedColumnMajor(self)

