
def convert_shape_to_symint(
    lst: Iterable[int | sympy.Expr],
) -> list[int | torch.SymInt]:
    """
    Takes a list of shapes from Inductor and converts them into symints (or just
    ints if all shapes are static).
    """
    return [convert_to_symint(i) for i in lst]

