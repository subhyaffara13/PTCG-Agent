
def squareCheckInputs(self: Tensor, f_name: str):
    if self.dim() < 2:
        raise AssertionError(
            f"{f_name}: The input tensor must have at least 2 dimensions, got {self.dim()}"
        )
    # Use torch._check to defer validation to runtime for unbacked symbolic dimensions.
    torch._check(
        self.size(-1) == self.size(-2),
        lambda: f"{f_name}: A must be batches of square matrices, "
        f"but they are {self.size(-2)} by {self.size(-1)} matrices",
    )

