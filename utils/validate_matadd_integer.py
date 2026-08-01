
def validate_matadd_integer(*args: MatrixExpr) -> None:
    """Validate matrix shape for addition only for integer values"""
    rows, cols = zip(*(x.shape for x in args))
    if len(set(filter(lambda x: isinstance(x, (int, Integer)), rows))) > 1:
        raise ShapeError(f"Matrices have mismatching shape: {rows}")
    if len(set(filter(lambda x: isinstance(x, (int, Integer)), cols))) > 1:
        raise ShapeError(f"Matrices have mismatching shape: {cols}")

