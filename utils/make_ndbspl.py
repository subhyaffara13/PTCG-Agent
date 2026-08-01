
def make_ndbspl(points, values, k=3, *, solver=ssl.gcrotmk, **solver_args):
    """Construct an interpolating NdBspline.

    Parameters
    ----------
    points : tuple of ndarrays of float, with shapes (m1,), ... (mN,)
        The points defining the regular grid in N dimensions. The points in
        each dimension (i.e. every element of the `points` tuple) must be
        strictly ascending or descending.
    values : ndarray of float, shape (m1, ..., mN, ...)
        The data on the regular grid in n dimensions.
    k : int, optional
        The spline degree. Must be odd. Default is cubic, k=3
    solver : a `scipy.sparse.linalg` solver (iterative or direct), optional.
        An iterative solver from `scipy.sparse.linalg` or a direct one,
        `sparse.sparse.linalg.spsolve`.
        Used to solve the sparse linear system
        ``design_matrix @ coefficients = rhs`` for the coefficients.
        Default is `scipy.sparse.linalg.gcrotmk`
    solver_args : dict, optional
        Additional arguments for the solver. The call signature is
        ``solver(csr_array, rhs_vector, **solver_args)``

    Returns
    -------
    spl : NdBSpline object

    Notes
    -----
    Boundary conditions are not-a-knot in all dimensions.
    """
    ndim = len(points)
    xi_shape = tuple(len(x) for x in points)

    try:
        len(k)
    except TypeError:
        # make k a tuple
        k = (k,)*ndim

    for d, point in enumerate(points):
        numpts = len(np.atleast_1d(point))
        if numpts <= k[d]:
            raise ValueError(f"There are {numpts} points in dimension {d},"
                             f" but order {k[d]} requires at least "
                             f" {k[d]+1} points per dimension.")

    t = tuple(_not_a_knot(np.asarray(points[d], dtype=float), k[d])
              for d in range(ndim))
    xvals = np.asarray([xv for xv in itertools.product(*points)], dtype=float)

    # construct the colocation matrix
    matr = NdBSpline.design_matrix(xvals, t, k)

    # Remove zeros from the sparse matrix
    # If k=1, then solve() doesn't take long enough for this to help
    if k[0] >= 3:
        matr.eliminate_zeros()

    # Solve for the coefficients given `values`.
    # Trailing dimensions: first ndim dimensions are data, the rest are batch
    # dimensions, so stack `values` into a 2D array for `spsolve` to undestand.
    v_shape = values.shape
    vals_shape = (prod(v_shape[:ndim]), prod(v_shape[ndim:]))
    vals = values.reshape(vals_shape)

    if solver != ssl.spsolve:
        solver = functools.partial(_iter_solve, solver=solver)
        if "atol" not in solver_args:
            # avoid a DeprecationWarning, grumble grumble
            solver_args["atol"] = 1e-6

    coef = solver(matr, vals, **solver_args)
    coef = coef.reshape(xi_shape + v_shape[ndim:])
    return NdBSpline(t, coef, k)

