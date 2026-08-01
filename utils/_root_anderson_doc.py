
def _root_anderson_doc():
    """
    Options
    -------
    nit : int, optional
        Number of iterations to make. If omitted (default), make as many
        as required to meet tolerances.
    disp : bool, optional
        Print status to stdout on every iteration.
    maxiter : int, optional
        Maximum number of iterations to make.
    ftol : float, optional
        Relative tolerance for the residual. If omitted, not used.
    fatol : float, optional
        Absolute tolerance (in max-norm) for the residual.
        If omitted, default is 6e-6.
    xtol : float, optional
        Relative minimum step size. If omitted, not used.
    xatol : float, optional
        Absolute minimum step size, as determined from the Jacobian
        approximation. If the step size is smaller than this, optimization
        is terminated as successful. If omitted, not used.
    tol_norm : function(vector) -> scalar, optional
        Norm to use in convergence check. Default is the maximum norm.
    line_search : {None, 'armijo' (default), 'wolfe'}, optional
        Which type of a line search to use to determine the step size in
        the direction given by the Jacobian approximation. Defaults to
        'armijo'.
    jac_options : dict, optional
        Options for the respective Jacobian approximation.

        alpha : float, optional
            Initial guess for the Jacobian is (-1/alpha).
        M : float, optional
            Number of previous vectors to retain. Defaults to 5.
        w0 : float, optional
            Regularization parameter for numerical stability.
            Compared to unity, good values of the order of 0.01.
    """
    pass

