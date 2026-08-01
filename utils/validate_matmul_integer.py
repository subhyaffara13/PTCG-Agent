
def validate_matmul_integer(*args: MatrixExpr) -> None:
    """Validate matrix shape for multiplication only for integer values"""
    for A, B in zip(args[:-1], args[1:]):
        i, j = A.cols, B.rows
        if isinstance(i, (int, Integer)) and isinstance(j, (int, Integer)) and i != j:
            raise ShapeError("Matrices are not aligned", i, j)

