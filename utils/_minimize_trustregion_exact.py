
def _minimize_trustregion_exact(fun, x0, args=(), jac=None, hess=None,
                                **trust_region_options):
    """
    Minimization of scalar function of one or more variables using
    a nearly exact trust-region algorithm.

    Options
    -------
    initial_trust_radius : float
        Initial trust-region radius.
    max_trust_radius : float
        Maximum value of the trust-region radius. No steps that are longer
        than this value will be proposed.
    eta : float
        Trust region related acceptance stringency for proposed steps.
    gtol : float
        Gradient norm must be less than ``gtol`` before successful
        termination.
    subproblem_maxiter : int, optional
        Maximum number of iterations to perform per subproblem. Only affects
        trust-exact. Default is 25.

        .. versionadded:: 1.17.0
    """
    if jac is None:
        raise ValueError('Jacobian is required for trust region '
                         'exact minimization.')
    if not callable(hess):
        raise ValueError('Hessian matrix is required for trust region '
                         'exact minimization.')
    return _minimize_trust_region(fun, x0, args=args, jac=jac, hess=hess,
                                  subproblem=IterativeSubproblem,
                                  **trust_region_options)

