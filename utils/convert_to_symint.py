
def convert_to_symint(i: int | sympy.Expr) -> int | torch.SymInt:
    """
    Like convert_shape_to_symint, but operates on a single expression.
    """
    from .virtualized import V

    return (
        i
        if isinstance(i, int)
        else (
            int(i)
            if isinstance(i, sympy.Integer)
            else V.graph.sizevars.shape_env.create_symintnode(i, hint=None)
        )
    )

