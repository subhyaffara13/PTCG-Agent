
def checkInputsSolver(A: Tensor, B: Tensor, left: bool, f_name: str):
    squareCheckInputs(A, f_name)
    checkIsMatrix(B, f_name)
    torch._check(
        A.size(-2) == B.size(-2) if left else A.size(-1) == B.size(-1),
        lambda: (
            f"{f_name}: Incompatible shapes of A and B for the equation "
            f"{'AX = B' if left else 'XA = B'}"
            f" ({A.size(-2)}x{A.size(-1)} and {B.size(-2)}x{B.size(-1)})"
        ),
    )

