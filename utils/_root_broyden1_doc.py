
def _root_broyden1_doc():
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
        reduction_method : str or tuple, optional
            Method used in ensuring that the rank of the Broyden
            matrix stays low. Can either be a string giving the
            name of the method, or a tuple of the form ``(method,
            param1, param2, ...)`` that gives the name of the
            method and values for additional parameters.

            Methods available:

            - ``restart``: drop all matrix columns. Has no extra parameters.
            - ``simple``: drop oldest matrix column. Has no extra parameters.
            - ``svd``: keep only the most significant SVD components.
              Takes an extra parameter, ``to_retain``, which determines the
              number of SVD components to retain when rank reduction is done.
              Default is ``max_rank - 2``.

        max_rank : int, optional
            Maximum rank for the Broyden matrix.
            Default is infinity (i.e., no rank reduction).

    Examples
    --------
    >>> def func(x):
    ...     return np.cos(x) + x[::-1] - [1, 2, 3, 4]
    ...
    >>> from scipy import optimize
    >>> res = optimize.root(func, [1, 1, 1, 1], method='broyden1', tol=1e-14)
    >>> x = res.x
    >>> x
    array([4.04674914, 3.91158389, 2.71791677, 1.61756251])
    >>> np.cos(x) + x[::-1]
    array([1., 2., 3., 4.])

    """
    pass

