
def print_iteration_nonlinear(iteration, nfev, cost, cost_reduction,
                              step_norm, optimality):
    if cost_reduction is None:
        cost_reduction = " " * 15
    else:
        cost_reduction = f"{cost_reduction:^15.2e}"

    if step_norm is None:
        step_norm = " " * 15
    else:
        step_norm = f"{step_norm:^15.2e}"

    print(f"{iteration:^15}{nfev:^15}{cost:^15.4e}{cost_reduction}{step_norm}{optimality:^15.2e}")

