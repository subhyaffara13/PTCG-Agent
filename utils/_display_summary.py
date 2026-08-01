
def _display_summary(message, status, fun, iteration):
    """
    Print the termination summary of the linear program

    Parameters
    ----------
    message : str
            A string descriptor of the exit status of the optimization.
    status : int
        An integer representing the exit status of the optimization::

                0 : Optimization terminated successfully
                1 : Iteration limit reached
                2 : Problem appears to be infeasible
                3 : Problem appears to be unbounded
                4 : Serious numerical difficulties encountered

    fun : float
        Value of the objective function.
    iteration : iteration
        The number of iterations performed.
    """
    print(message)
    if status in (0, 1):
        print(f"         Current function value: {fun: <12.6f}")
    print(f"         Iterations: {iteration:d}")

