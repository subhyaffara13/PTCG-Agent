
def _parse_linear_solver(linear_solver):
    """Helper function to retrieve a specified linear solver."""
    if callable(linear_solver):
        return linear_solver
    return lambda A, b: Matrix.solve(A, b, method=linear_solver)

