
def _print_step(message, pb, x, fun_val, r_val, n_eval, n_iter):
    """
    Print information about the current state of the optimization process.
    """
    print()
    print(f"{message}.")
    print(f"Number of function evaluations: {n_eval}.")
    print(f"Number of iterations: {n_iter}.")
    if not pb.is_feasibility:
        print(f"Least value of {pb.fun_name}: {fun_val}.")
    print(f"Maximum constraint violation: {r_val}.")
    with np.printoptions(**PRINT_OPTIONS):
        print(f"Corresponding point: {x}.")

