
def _display_iter(rho_p, rho_d, rho_g, alpha, rho_mu, obj, header=False):
    """
    Print indicators of optimization status to the console.

    Parameters
    ----------
    rho_p : float
        The (normalized) primal feasibility, see [4] 4.5
    rho_d : float
        The (normalized) dual feasibility, see [4] 4.5
    rho_g : float
        The (normalized) duality gap, see [4] 4.5
    alpha : float
        The step size, see [4] 4.3
    rho_mu : float
        The (normalized) path parameter, see [4] 4.5
    obj : float
        The objective function value of the current iterate
    header : bool
        True if a header is to be printed

    References
    ----------
    .. [4] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.

    """
    if header:
        print("Primal Feasibility ",
              "Dual Feasibility   ",
              "Duality Gap        ",
              "Step            ",
              "Path Parameter     ",
              "Objective          ")

    # no clue why this works
    fmt = '{0:<20.13}{1:<20.13}{2:<20.13}{3:<17.13}{4:<20.13}{5:<20.13}'
    print(fmt.format(
        float(rho_p),
        float(rho_d),
        float(rho_g),
        alpha if isinstance(alpha, str) else float(alpha),
        float(rho_mu),
        float(obj)))


def _display_iter(phase, iteration, slack, con, fun):
    """
    Print indicators of optimization status to the console.
    """
    header = True if not iteration % 20 else False

    if header:
        print("Phase",
              "Iteration",
              "Minimum Slack      ",
              "Constraint Residual",
              "Objective          ")

    # :<X.Y left aligns Y digits in X digit spaces
    fmt = '{0:<6}{1:<10}{2:<20.13}{3:<20.13}{4:<20.13}'
    try:
        slack = np.min(slack)
    except ValueError:
        slack = "NA"
    print(fmt.format(phase, iteration, slack, np.linalg.norm(con), fun))

