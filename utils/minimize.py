import itertools
from typing import Any, Callable

def minimize(
    target_func,
    initial_parameters,
    reference_parameters,
    step_func,
    max_step=2,
    verbose=False,
    all_values=None,
):
    """Find a dict of parameters that minimizes the target function using
    the initial dict of parameters and a step function that progresses
    a specified parameter in a dict of parameters.

    Parameters
    ----------
    target_func (callable): a functional with the signature
      ``target_func(parameters: dict) -> float``
    initial_parameters (dict): a set of parameters used as an initial
      value to the minimization process.
    reference_parameters (dict): a set of parameters used as an
      reference value with respect to which the speed up is computed.
    step_func (callable): a functional with the signature
      ``step_func(parameter_name:str, parameter_value:int, direction:int, parameters:dict) -> int``
      that increments or decrements (when ``direction`` is positive or
      negative, respectively) the parameter with given name and value.
      When return value is equal to ``parameter_value``, it means that
      no step along the given direction can be made.

    Returns
    -------
    parameters (dict): a set of parameters that minimizes the target
      function.
    speedup_incr (float): a speedup change given in percentage.
    timing (float): the value of the target function at the parameters.
    sensitivity_message (str): a message containing sensitivity.
      information of parameters around the target function minimizer.
    """

    def to_key(parameters):
        return tuple(parameters[k] for k in sorted(parameters))

    def from_key(key, parameters):
        return dict(zip(sorted(parameters), key, strict=True))

    if all_values is None:
        all_values = {}

    directions = list(range(-max_step, max_step + 1))
    names = sorted(initial_parameters)
    all_directions = []
    for d_tuple in itertools.product(*((directions,) * len(names))):
        dist = sum(map(abs, d_tuple))
        if dist > 0 and dist <= max_step:
            all_directions.append((dist, d_tuple))
    all_directions.sort()

    try:
        reference_target = target_func(reference_parameters)
    except Exception as msg:
        if verbose and "out of resource" not in str(msg):
            print(f"{reference_parameters=} lead to failure: {msg}.")
        reference_target = None

    if reference_target is not None:
        all_values[to_key(reference_parameters)] = reference_target

    parameters = initial_parameters
    try:
        initial_target = target_func(parameters)
    except Exception as msg:
        if reference_target is None:
            if verbose:
                print(
                    f"{initial_parameters=} lead to failure: {msg}. Optimization failed!"
                )
            return {}, -1, -1, f"{msg}"
        if verbose and "out of resource" not in str(msg):
            print(
                f"{initial_parameters=} lead to failure: {msg}. Using reference parameters instead of initial parameters."
            )
        parameters = reference_parameters
        initial_target = reference_target

    if reference_target is None:
        if verbose:
            print("Using initial parameters instead of reference parameters.")
        reference_target = initial_target

    initial_key = to_key(parameters)
    minimal_target = all_values[initial_key] = initial_target
    pbar = tqdm(
        total=len(all_directions),
        desc="Tuning...",
        disable=not verbose,
        ncols=75,
    )
    while True:
        for i, (_, d_tuple) in enumerate(all_directions):
            pbar.update(1)
            next_parameters = parameters.copy()
            for name, direction in zip(names, d_tuple, strict=True):
                value = next_parameters[name]
                if direction == 0:
                    continue
                next_value = step_func(name, value, direction, parameters)
                if next_value == value:
                    break
                next_parameters[name] = next_value
            else:
                next_key = to_key(next_parameters)
                if next_key in all_values:
                    continue
                try:
                    next_target = target_func(next_parameters)
                except Exception as msg:
                    all_values[next_key] = str(msg)
                    if verbose and "out of resource" not in str(msg):
                        print(f"{next_parameters=} lead to failure: {msg}. Skipping.")
                    continue
                all_values[next_key] = next_target

                if next_target < minimal_target:
                    minimal_target = next_target
                    parameters = next_parameters
                    # pyrefly: ignore [unsupported-operation]
                    pbar.total += i + 1
                    break
        else:
            # ensure stable minimizer:
            minimizer_keys = {
                k
                for k, v in all_values.items()
                if isinstance(v, float) and abs(1 - v / minimal_target) < 0.001
            }
            minimizer_key = (
                initial_key if initial_key in minimizer_keys else min(minimizer_keys)
            )
            parameters = from_key(minimizer_key, parameters)
            speedup_incr = (1 - minimal_target / reference_target) * 100
            if speedup_incr < 0:
                if verbose:
                    print(
                        f"{speedup_incr=} is negative. Rerunning minimize with reference parameters as initial parameters."
                    )
                return minimize(
                    target_func,
                    reference_parameters,
                    reference_parameters,
                    step_func,
                    max_step=max_step,
                    verbose=verbose,
                    all_values=all_values,
                )
            sensitivity = []
            for name in parameters:
                value = parameters[name]
                rel_diffs = []
                for direction in range(-max_step, max_step + 1):
                    if direction == 0:
                        continue
                    next_value = step_func(name, value, direction, parameters)
                    if next_value == value:
                        rel_diffs.append(0)
                        continue
                    next_parameters = parameters.copy()
                    next_parameters[name] = next_value
                    next_key = to_key(next_parameters)
                    next_target = all_values.get(next_key)
                    if next_target is None or isinstance(next_target, str):
                        rel_diffs.append(0)
                        continue
                    rel_diff = (next_target / minimal_target - 1) * 100
                    rel_diffs.append(rel_diff)
                sensitivity.append((max(rel_diffs), rel_diffs, name))

            sensitivity_message = [f"timing0={initial_target:.3f}"]
            for _, rel_diffs, name in sorted(sensitivity, reverse=True):
                left_diffs = "|".join(
                    [f"{rel_diff:.1f}" for rel_diff in rel_diffs[:max_step]]
                )
                right_diffs = "|".join(
                    [f"{rel_diff:.1f}" for rel_diff in rel_diffs[max_step:]]
                )
                sensitivity_message.append(
                    f"{name}={parameters[name]} ({left_diffs}...{right_diffs} %)"
                )
            sensitivity_message = ", ".join(sensitivity_message)
            return parameters, speedup_incr, minimal_target, sensitivity_message


def minimize(
    *rules: Callable[[_S], _T],
    objective=_identity
) -> Callable[[_S], _T]:
    """ Select result of rules that minimizes objective

    >>> from sympy.strategies import minimize
    >>> inc = lambda x: x + 1
    >>> dec = lambda x: x - 1
    >>> rl = minimize(inc, dec)
    >>> rl(4)
    3

    >>> rl = minimize(inc, dec, objective=lambda x: -x)  # maximize
    >>> rl(4)
    5
    """
    def minrule(expr: _S) -> _T:
        return min([rule(expr) for rule in rules], key=objective)
    return minrule


def minimize(fun, x0, args=(), method=None, jac=None, hess=None,
             hessp=None, bounds=None, constraints=(), tol=None,
             callback=None, options=None):
    """Minimization of scalar function of one or more variables.

    Parameters
    ----------
    fun : callable
        The objective function to be minimized::

            fun(x, *args) -> float

        where ``x`` is a 1-D array with shape (n,) and ``args``
        is a tuple of the fixed parameters needed to completely
        specify the function.

        Suppose the callable has signature ``f0(x, *my_args, **my_kwargs)``, where
        ``my_args`` and ``my_kwargs`` are required positional and keyword arguments.
        Rather than passing ``f0`` as the callable, wrap it to accept
        only ``x``; e.g., pass ``fun=lambda x: f0(x, *my_args, **my_kwargs)`` as the
        callable, where ``my_args`` (tuple) and ``my_kwargs`` (dict) have been
        gathered before invoking this function.
    x0 : ndarray, shape (n,)
        Initial guess. Array of real elements of size (n,),
        where ``n`` is the number of independent variables.
    args : tuple, optional
        Extra arguments passed to the objective function and its
        derivatives (`fun`, `jac` and `hess` functions).
    method : str or callable, optional
        Type of solver.  Should be one of

        - 'Nelder-Mead' :ref:`(see here) <optimize.minimize-neldermead>`
        - 'Powell'      :ref:`(see here) <optimize.minimize-powell>`
        - 'CG'          :ref:`(see here) <optimize.minimize-cg>`
        - 'BFGS'        :ref:`(see here) <optimize.minimize-bfgs>`
        - 'Newton-CG'   :ref:`(see here) <optimize.minimize-newtoncg>`
        - 'L-BFGS-B'    :ref:`(see here) <optimize.minimize-lbfgsb>`
        - 'TNC'         :ref:`(see here) <optimize.minimize-tnc>`
        - 'COBYLA'      :ref:`(see here) <optimize.minimize-cobyla>`
        - 'COBYQA'      :ref:`(see here) <optimize.minimize-cobyqa>`
        - 'SLSQP'       :ref:`(see here) <optimize.minimize-slsqp>`
        - 'trust-constr':ref:`(see here) <optimize.minimize-trustconstr>`
        - 'dogleg'      :ref:`(see here) <optimize.minimize-dogleg>`
        - 'trust-ncg'   :ref:`(see here) <optimize.minimize-trustncg>`
        - 'trust-exact' :ref:`(see here) <optimize.minimize-trustexact>`
        - 'trust-krylov' :ref:`(see here) <optimize.minimize-trustkrylov>`
        - custom - a callable object, see below for description.

        If not given, chosen to be one of ``BFGS``, ``L-BFGS-B``, ``SLSQP``,
        depending on whether or not the problem has constraints or bounds.
    jac : {callable,  '2-point', '3-point', 'cs', bool}, optional
        Method for computing the gradient vector. Only for CG, BFGS,
        Newton-CG, L-BFGS-B, TNC, SLSQP, dogleg, trust-ncg, trust-krylov,
        trust-exact and trust-constr.
        If it is a callable, it should be a function that returns the gradient
        vector::

            jac(x, *args) -> array_like, shape (n,)

        where ``x`` is an array with shape (n,) and ``args`` is a tuple with
        the fixed parameters. If `jac` is a Boolean and is True, `fun` is
        assumed to return a tuple ``(f, g)`` containing the objective
        function and the gradient.
        Methods 'Newton-CG', 'trust-ncg', 'dogleg', 'trust-exact', and
        'trust-krylov' require that either a callable be supplied, or that
        `fun` return the objective and gradient.
        If None or False, the gradient will be estimated using 2-point finite
        difference estimation with an absolute step size.
        Alternatively, the keywords  {'2-point', '3-point', 'cs'} can be used
        to select a finite difference scheme for numerical estimation of the
        gradient with a relative step size. These finite difference schemes
        obey any specified `bounds`.
    hess : {callable, '2-point', '3-point', 'cs', HessianUpdateStrategy}, optional
        Method for computing the Hessian matrix. Only for Newton-CG, dogleg,
        trust-ncg, trust-krylov, trust-exact and trust-constr.
        If it is callable, it should return the Hessian matrix::

            hess(x, *args) -> {LinearOperator, spmatrix, array}, (n, n)

        where ``x`` is a (n,) ndarray and ``args`` is a tuple with the fixed
        parameters.
        The keywords {'2-point', '3-point', 'cs'} can also be used to select
        a finite difference scheme for numerical estimation of the hessian.
        Alternatively, objects implementing the `HessianUpdateStrategy`
        interface can be used to approximate the Hessian. Available
        quasi-Newton methods implementing this interface are:

        - `BFGS`
        - `SR1`

        Not all of the options are available for each of the methods; for
        availability refer to the notes.
    hessp : callable, optional
        Hessian of objective function times an arbitrary vector p. Only for
        Newton-CG, trust-ncg, trust-krylov, trust-constr.
        Only one of `hessp` or `hess` needs to be given. If `hess` is
        provided, then `hessp` will be ignored. `hessp` must compute the
        Hessian times an arbitrary vector::

            hessp(x, p, *args) ->  ndarray shape (n,)

        where ``x`` is a (n,) ndarray, ``p`` is an arbitrary vector with
        dimension (n,) and ``args`` is a tuple with the fixed
        parameters.
    bounds : sequence or `Bounds`, optional
        Bounds on variables for Nelder-Mead, L-BFGS-B, TNC, SLSQP, Powell,
        trust-constr, COBYLA, and COBYQA methods. There are two ways to specify
        the bounds:

        1. Instance of `Bounds` class.
        2. Sequence of ``(min, max)`` pairs for each element in `x`. None
           is used to specify no bound.

    constraints : {Constraint, dict} or List of {Constraint, dict}, optional
        Constraints definition. Only for COBYLA, COBYQA, SLSQP and trust-constr.

        Constraints for 'trust-constr', 'cobyqa', and 'cobyla' are defined as a single
        object or a list of objects specifying constraints to the optimization problem.
        Available constraints are:

        - `LinearConstraint`
        - `NonlinearConstraint`

        Constraints for COBYLA, SLSQP are defined as a list of dictionaries.
        Each dictionary with fields:

        type : str
            Constraint type: 'eq' for equality, 'ineq' for inequality.
        fun : callable
            The function defining the constraint.
        jac : callable, optional
            The Jacobian of `fun` (only for SLSQP).
        args : sequence, optional
            Extra arguments to be passed to the function and Jacobian.

        Equality constraint means that the constraint function result is to
        be zero whereas inequality means that it is to be non-negative.

    tol : float, optional
        Tolerance for termination. When `tol` is specified, the selected
        minimization algorithm sets some relevant solver-specific tolerance(s)
        equal to `tol`. For detailed control, use solver-specific
        options.
    callback : callable, optional
        A callable called after each iteration.

        All methods except TNC support a callable with
        the signature::

            callback(intermediate_result: OptimizeResult)

        where ``intermediate_result`` is a keyword parameter containing an
        `OptimizeResult` with attributes ``x`` and ``fun``, the present values
        of the parameter vector and objective function. Not all attributes of
        `OptimizeResult` may be present. The name of the parameter must be
        ``intermediate_result`` for the callback to be passed an `OptimizeResult`.
        These methods will also terminate if the callback raises ``StopIteration``.

        All methods except trust-constr (also) support a signature like::

            callback(xk)

        where ``xk`` is the current parameter vector.

        Introspection is used to determine which of the signatures above to
        invoke.
    options : dict, optional
        A dictionary of solver options. All methods except `TNC` accept the
        following generic options:

        maxiter : int
            Maximum number of iterations to perform. Depending on the
            method each iteration may use several function evaluations.

            For `TNC` use `maxfun` instead of `maxiter`.
        disp : bool
            Set to True to print convergence messages.

        For method-specific options, see :func:`show_options()`.

    Returns
    -------
    res : OptimizeResult
        The optimization result represented as a ``OptimizeResult`` object.
        Important attributes are: ``x`` the solution array, ``success`` a
        Boolean flag indicating if the optimizer exited successfully and
        ``message`` which describes the cause of the termination. See
        `OptimizeResult` for a description of other attributes.

    See Also
    --------
    minimize_scalar : Interface to minimization algorithms for scalar
        univariate functions
    show_options : Additional options accepted by the solvers

    Notes
    -----
    This section describes the available solvers that can be selected by the
    'method' parameter. The default method is *BFGS*.

    **Unconstrained minimization**

    Method :ref:`CG <optimize.minimize-cg>` uses a nonlinear conjugate
    gradient algorithm by Polak and Ribiere, a variant of the
    Fletcher-Reeves method described in [5]_ pp.120-122. Only the
    first derivatives are used.

    Method :ref:`BFGS <optimize.minimize-bfgs>` uses the quasi-Newton
    method of Broyden, Fletcher, Goldfarb, and Shanno (BFGS) [5]_
    pp. 136. It uses the first derivatives only. BFGS has proven good
    performance even for non-smooth optimizations. This method also
    returns an approximation of the Hessian inverse, stored as
    `hess_inv` in the OptimizeResult object.

    Method :ref:`Newton-CG <optimize.minimize-newtoncg>` uses a
    Newton-CG algorithm [5]_ pp. 168 (also known as the truncated
    Newton method). It uses a CG method to the compute the search
    direction. See also *TNC* method for a box-constrained
    minimization with a similar algorithm. Suitable for large-scale
    problems.

    Method :ref:`dogleg <optimize.minimize-dogleg>` uses the dog-leg
    trust-region algorithm [5]_ for unconstrained minimization. This
    algorithm requires the gradient and Hessian; furthermore the
    Hessian is required to be positive definite.

    Method :ref:`trust-ncg <optimize.minimize-trustncg>` uses the
    Newton conjugate gradient trust-region algorithm [5]_ for
    unconstrained minimization. This algorithm requires the gradient
    and either the Hessian or a function that computes the product of
    the Hessian with a given vector. Suitable for large-scale problems.

    Method :ref:`trust-krylov <optimize.minimize-trustkrylov>` uses
    the Newton GLTR trust-region algorithm [14]_, [15]_ for unconstrained
    minimization. This algorithm requires the gradient
    and either the Hessian or a function that computes the product of
    the Hessian with a given vector. Suitable for large-scale problems.
    On indefinite problems it requires usually less iterations than the
    `trust-ncg` method and is recommended for medium and large-scale problems.

    Method :ref:`trust-exact <optimize.minimize-trustexact>`
    is a trust-region method for unconstrained minimization in which
    quadratic subproblems are solved almost exactly [13]_. This
    algorithm requires the gradient and the Hessian (which is
    *not* required to be positive definite). It is, in many
    situations, the Newton method to converge in fewer iterations
    and the most recommended for small and medium-size problems.

    **Bound-Constrained minimization**

    Method :ref:`Nelder-Mead <optimize.minimize-neldermead>` uses the
    Simplex algorithm [1]_, [2]_. This algorithm is robust in many
    applications. However, if numerical computation of derivative can be
    trusted, other algorithms using the first and/or second derivatives
    information might be preferred for their better performance in
    general.

    Method :ref:`L-BFGS-B <optimize.minimize-lbfgsb>` uses the L-BFGS-B
    algorithm [6]_, [7]_ for bound constrained minimization.

    Method :ref:`Powell <optimize.minimize-powell>` is a modification
    of Powell's method [3]_, [4]_ which is a conjugate direction
    method. It performs sequential one-dimensional minimizations along
    each vector of the directions set (`direc` field in `options` and
    `info`), which is updated at each iteration of the main
    minimization loop. The function need not be differentiable, and no
    derivatives are taken. If bounds are not provided, then an
    unbounded line search will be used. If bounds are provided and
    the initial guess is within the bounds, then every function
    evaluation throughout the minimization procedure will be within
    the bounds. If bounds are provided, the initial guess is outside
    the bounds, and `direc` is full rank (default has full rank), then
    some function evaluations during the first iteration may be
    outside the bounds, but every function evaluation after the first
    iteration will be within the bounds. If `direc` is not full rank,
    then some parameters may not be optimized and the solution is not
    guaranteed to be within the bounds.

    Method :ref:`TNC <optimize.minimize-tnc>` uses a truncated Newton
    algorithm [5]_, [8]_ to minimize a function with variables subject
    to bounds. This algorithm uses gradient information; it is also
    called Newton Conjugate-Gradient. It differs from the *Newton-CG*
    method described above as it wraps a C implementation and allows
    each variable to be given upper and lower bounds.

    **Constrained Minimization**

    Method :ref:`COBYLA <optimize.minimize-cobyla>` uses the PRIMA
    implementation [19]_ of the
    Constrained Optimization BY Linear Approximation (COBYLA) method
    [9]_, [10]_, [11]_. The algorithm is based on linear
    approximations to the objective function and each constraint.

    Method :ref:`COBYQA <optimize.minimize-cobyqa>` uses the Constrained
    Optimization BY Quadratic Approximations (COBYQA) method [18]_. The
    algorithm is a derivative-free trust-region SQP method based on quadratic
    approximations to the objective function and each nonlinear constraint. The
    bounds are treated as unrelaxable constraints, in the sense that the
    algorithm always respects them throughout the optimization process.

    Method :ref:`SLSQP <optimize.minimize-slsqp>` uses Sequential
    Least SQuares Programming to minimize a function of several
    variables with any combination of bounds, equality and inequality
    constraints. The method wraps the SLSQP Optimization subroutine
    originally implemented by Dieter Kraft [12]_. Note that the
    wrapper handles infinite values in bounds by converting them into
    large floating values.

    Method :ref:`trust-constr <optimize.minimize-trustconstr>` is a
    trust-region algorithm for constrained optimization. It switches
    between two implementations depending on the problem definition.
    It is the most versatile constrained minimization algorithm
    implemented in SciPy and the most appropriate for large-scale problems.
    For equality constrained problems it is an implementation of Byrd-Omojokun
    Trust-Region SQP method described in [17]_ and in [5]_, p. 549. When
    inequality constraints are imposed as well, it switches to the trust-region
    interior point method described in [16]_. This interior point algorithm,
    in turn, solves inequality constraints by introducing slack variables
    and solving a sequence of equality-constrained barrier problems
    for progressively smaller values of the barrier parameter.
    The previously described equality constrained SQP method is
    used to solve the subproblems with increasing levels of accuracy
    as the iterate gets closer to a solution.

    **Finite-Difference Options**

    For Method :ref:`trust-constr <optimize.minimize-trustconstr>`
    the gradient and the Hessian may be approximated using
    three finite-difference schemes: {'2-point', '3-point', 'cs'}.
    The scheme 'cs' is, potentially, the most accurate but it
    requires the function to correctly handle complex inputs and to
    be differentiable in the complex plane. The scheme '3-point' is more
    accurate than '2-point' but requires twice as many operations. If the
    gradient is estimated via finite-differences the Hessian must be
    estimated using one of the quasi-Newton strategies.

    **Method specific options for the** `hess` **keyword**

    +--------------+------+----------+-------------------------+-----+
    | method/Hess  | None | callable | '2-point/'3-point'/'cs' | HUS |
    +==============+======+==========+=========================+=====+
    | Newton-CG    | x    | (n, n)   | x                       | x   |
    |              |      | LO       |                         |     |
    +--------------+------+----------+-------------------------+-----+
    | dogleg       |      | (n, n)   |                         |     |
    +--------------+------+----------+-------------------------+-----+
    | trust-ncg    |      | (n, n)   | x                       | x   |
    +--------------+------+----------+-------------------------+-----+
    | trust-krylov |      | (n, n)   | x                       | x   |
    +--------------+------+----------+-------------------------+-----+
    | trust-exact  |      | (n, n)   |                         |     |
    +--------------+------+----------+-------------------------+-----+
    | trust-constr | x    | (n, n)   |  x                      | x   |
    |              |      | LO       |                         |     |
    |              |      | sp       |                         |     |
    +--------------+------+----------+-------------------------+-----+

    where LO=LinearOperator, sp=Sparse matrix, HUS=HessianUpdateStrategy

    **Custom minimizers**

    It may be useful to pass a custom minimization method, for example
    when using a frontend to this method such as `scipy.optimize.basinhopping`
    or a different library.  You can simply pass a callable as the ``method``
    parameter.

    The callable is called as ``method(fun, x0, args, **kwargs, **options)``
    where ``kwargs`` corresponds to any other parameters passed to `minimize`
    (such as `callback`, `hess`, etc.), except the `options` dict, which has
    its contents also passed as `method` parameters pair by pair.  Also, if
    `jac` has been passed as a bool type, `jac` and `fun` are mangled so that
    `fun` returns just the function values and `jac` is converted to a function
    returning the Jacobian.  The method shall return an `OptimizeResult`
    object.

    The provided `method` callable must be able to accept (and possibly ignore)
    arbitrary parameters; the set of parameters accepted by `minimize` may
    expand in future versions and then these parameters will be passed to
    the method.  You can find an example in the scipy.optimize tutorial.

    References
    ----------
    .. [1] Nelder, J A, and R Mead. 1965. A Simplex Method for Function
        Minimization. The Computer Journal 7: 308-13.
    .. [2] Wright M H. 1996. Direct search methods: Once scorned, now
        respectable, in Numerical Analysis 1995: Proceedings of the 1995
        Dundee Biennial Conference in Numerical Analysis (Eds. D F
        Griffiths and G A Watson). Addison Wesley Longman, Harlow, UK.
        191-208.
    .. [3] Powell, M J D. 1964. An efficient method for finding the minimum of
       a function of several variables without calculating derivatives. The
       Computer Journal 7: 155-162.
    .. [4] Press W, S A Teukolsky, W T Vetterling and B P Flannery.
       Numerical Recipes (any edition), Cambridge University Press.
    .. [5] Nocedal, J, and S J Wright. 2006. Numerical Optimization.
       Springer New York.
    .. [6] Byrd, R H and P Lu and J. Nocedal. 1995. A Limited Memory
       Algorithm for Bound Constrained Optimization. SIAM Journal on
       Scientific and Statistical Computing 16 (5): 1190-1208.
    .. [7] Zhu, C and R H Byrd and J Nocedal. 1997. L-BFGS-B: Algorithm
       778: L-BFGS-B, FORTRAN routines for large scale bound constrained
       optimization. ACM Transactions on Mathematical Software 23 (4):
       550-560.
    .. [8] Nash, S G. Newton-Type Minimization Via the Lanczos Method.
       1984. SIAM Journal of Numerical Analysis 21: 770-778.
    .. [9] Powell, M J D. A direct search optimization method that models
       the objective and constraint functions by linear interpolation.
       1994. Advances in Optimization and Numerical Analysis, eds. S. Gomez
       and J-P Hennart, Kluwer Academic (Dordrecht), 51-67.
    .. [10] Powell M J D. Direct search algorithms for optimization
       calculations. 1998. Acta Numerica 7: 287-336.
    .. [11] Powell M J D. A view of algorithms for optimization without
       derivatives. 2007.Cambridge University Technical Report DAMTP
       2007/NA03
    .. [12] Kraft, D. A software package for sequential quadratic
       programming. 1988. Tech. Rep. DFVLR-FB 88-28, DLR German Aerospace
       Center -- Institute for Flight Mechanics, Koln, Germany.
    .. [13] Conn, A. R., Gould, N. I., and Toint, P. L.
       Trust region methods. 2000. Siam. pp. 169-200.
    .. [14] F. Lenders, C. Kirches, A. Potschka: "trlib: A vector-free
       implementation of the GLTR method for iterative solution of
       the trust region problem", :arxiv:`1611.04718`
    .. [15] N. Gould, S. Lucidi, M. Roma, P. Toint: "Solving the
       Trust-Region Subproblem using the Lanczos Method",
       SIAM J. Optim., 9(2), 504--525, (1999).
    .. [16] Byrd, Richard H., Mary E. Hribar, and Jorge Nocedal. 1999.
        An interior point algorithm for large-scale nonlinear  programming.
        SIAM Journal on Optimization 9.4: 877-900.
    .. [17] Lalee, Marucha, Jorge Nocedal, and Todd Plantenga. 1998. On the
        implementation of an algorithm for large-scale equality constrained
        optimization. SIAM Journal on Optimization 8.3: 682-706.
    .. [18] Ragonneau, T. M. *Model-Based Derivative-Free Optimization Methods
        and Software*. PhD thesis, Department of Applied Mathematics, The Hong
        Kong Polytechnic University, Hong Kong, China, 2022. URL:
        https://theses.lib.polyu.edu.hk/handle/200/12294.
    .. [19] Zhang, Z. "PRIMA: Reference Implementation for Powell's Methods with
        Modernization and Amelioration", https://www.libprima.net,
        :doi:`10.5281/zenodo.8052654`
    .. [20] Karush-Kuhn-Tucker conditions,
        https://en.wikipedia.org/wiki/Karush%E2%80%93Kuhn%E2%80%93Tucker_conditions

    Examples
    --------
    Let us consider the problem of minimizing the Rosenbrock function. This
    function (and its respective derivatives) is implemented in `rosen`
    (resp. `rosen_der`, `rosen_hess`) in the `scipy.optimize`.

    >>> from scipy.optimize import minimize, rosen, rosen_der

    A simple application of the *Nelder-Mead* method is:

    >>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
    >>> res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)
    >>> res.x
    array([ 1.,  1.,  1.,  1.,  1.])

    Now using the *BFGS* algorithm, using the first derivative and a few
    options:

    >>> res = minimize(rosen, x0, method='BFGS', jac=rosen_der,
    ...                options={'gtol': 1e-6, 'disp': True})
    Optimization terminated successfully.
             Current function value: 0.000000
             Iterations: 26
             Function evaluations: 31
             Gradient evaluations: 31
    >>> res.x
    array([ 1.,  1.,  1.,  1.,  1.])
    >>> print(res.message)
    Optimization terminated successfully.
    >>> res.hess_inv
    array([
        [ 0.00749589,  0.01255155,  0.02396251,  0.04750988,  0.09495377],  # may vary
        [ 0.01255155,  0.02510441,  0.04794055,  0.09502834,  0.18996269],
        [ 0.02396251,  0.04794055,  0.09631614,  0.19092151,  0.38165151],
        [ 0.04750988,  0.09502834,  0.19092151,  0.38341252,  0.7664427 ],
        [ 0.09495377,  0.18996269,  0.38165151,  0.7664427,   1.53713523]
    ])

    Next, consider a minimization problem with several constraints (namely
    Example 16.4 from [5]_). The objective function is:

    >>> fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2

    There are three constraints defined as:

    >>> cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},
    ...         {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
    ...         {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})

    And variables must be positive, hence the following bounds:

    >>> bnds = ((0, None), (0, None))

    The optimization problem is solved using the SLSQP method as:

    >>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)

    It should converge to the theoretical solution ``[1.4 ,1.7]``. *SLSQP* also
    returns the multipliers that are used in the solution of the problem. These
    multipliers, when the problem constraints are linear, can be thought of as the
    Karush-Kuhn-Tucker (KKT) multipliers, which are a generalization
    of Lagrange multipliers to inequality-constrained optimization problems ([20]_).

    Notice that at the solution, the first constraint is active. Let's evaluate the
    function at solution:

    >>> cons[0]['fun'](res.x)
    np.float64(1.4901224698604665e-09)

    Also, notice that at optimality there is a non-zero multiplier:

    >>> res.multipliers
    array([0.8, 0. , 0. ])

    This can be understood as the local sensitivity of the optimal value of the
    objective function with respect to changes in the first constraint. If we
    tighten the constraint by a small amount ``eps``:

    >>> eps = 0.01
    >>> cons[0]['fun'] = lambda x: x[0] - 2 * x[1] + 2 - eps

    we expect the optimal value of the objective function to increase by
    approximately ``eps * res.multipliers[0]``:

    >>> eps * res.multipliers[0]  # Expected change in f0
    np.float64(0.008000000027153205)
    >>> f0 = res.fun  # Keep track of the previous optimal value
    >>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds, constraints=cons)
    >>> f1 = res.fun  # New optimal value
    >>> f1 - f0
    np.float64(0.008019998807885509)

    """
    x0 = np.atleast_1d(np.asarray(x0))

    if x0.ndim != 1:
        raise ValueError("'x0' must only have one dimension.")

    if x0.dtype.kind in np.typecodes["AllInteger"]:
        x0 = np.asarray(x0, dtype=float)

    if not isinstance(args, tuple):
        args = (args,)

    if method is None:
        # Select automatically
        if constraints:
            method = 'SLSQP'
        elif bounds is not None:
            method = 'L-BFGS-B'
        else:
            method = 'BFGS'

    if callable(method):
        meth = "_custom"
    else:
        meth = method.lower()

    if options is None:
        options = {}
    # check if optional parameters are supported by the selected method
    # - jac
    if meth in ('nelder-mead', 'powell', 'cobyla', 'cobyqa') and bool(jac):
        warn(f'Method {method} does not use gradient information (jac).',
             RuntimeWarning, stacklevel=2)
    # - hess
    if meth not in ('newton-cg', 'dogleg', 'trust-ncg', 'trust-constr',
                    'trust-krylov', 'trust-exact', '_custom') and hess is not None:
        warn(f'Method {method} does not use Hessian information (hess).',
             RuntimeWarning, stacklevel=2)
    # - hessp
    if meth not in ('newton-cg', 'trust-ncg', 'trust-constr',
                    'trust-krylov', '_custom') \
       and hessp is not None:
        warn(f'Method {method} does not use Hessian-vector product'
             ' information (hessp).',
             RuntimeWarning, stacklevel=2)
    # - constraints or bounds
    if (meth not in ('cobyla', 'cobyqa', 'slsqp', 'trust-constr', '_custom') and
            np.any(constraints)):
        warn(f'Method {method} cannot handle constraints.',
             RuntimeWarning, stacklevel=2)
    if meth not in (
            'nelder-mead', 'powell', 'l-bfgs-b', 'cobyla', 'cobyqa', 'slsqp',
            'tnc', 'trust-constr', '_custom') and bounds is not None:
        warn(f'Method {method} cannot handle bounds.',
             RuntimeWarning, stacklevel=2)
    # - return_all
    if (meth in ('l-bfgs-b', 'tnc', 'cobyla', 'cobyqa', 'slsqp') and
            options.get('return_all', False)):
        warn(f'Method {method} does not support the return_all option.',
             RuntimeWarning, stacklevel=2)

    # check gradient vector
    if callable(jac):
        pass
    elif jac is True:
        # fun returns func and grad
        fun = MemoizeJac(fun)
        jac = fun.derivative
    elif (jac in FD_METHODS and
          meth in ['trust-constr', 'bfgs', 'cg', 'l-bfgs-b', 'tnc', 'slsqp']):
        # finite differences with relative step
        pass
    elif meth in ['trust-constr']:
        # default jac calculation for this method
        jac = '2-point'
    elif jac is None or bool(jac) is False:
        # this will cause e.g. LBFGS to use forward difference, absolute step
        jac = None
    else:
        # default if jac option is not understood
        jac = None

    # set default tolerances
    if tol is not None:
        options = dict(options)
        if meth == 'nelder-mead':
            options.setdefault('xatol', tol)
            options.setdefault('fatol', tol)
        if meth in ('newton-cg', 'powell', 'tnc'):
            options.setdefault('xtol', tol)
        if meth in ('powell', 'l-bfgs-b', 'tnc', 'slsqp'):
            options.setdefault('ftol', tol)
        if meth in ('bfgs', 'cg', 'l-bfgs-b', 'tnc', 'dogleg',
                    'trust-ncg', 'trust-exact', 'trust-krylov'):
            options.setdefault('gtol', tol)
        if meth in ('cobyla', '_custom'):
            options.setdefault('tol', tol)
        if meth == 'cobyqa':
            options.setdefault('final_tr_radius', tol)
        if meth == 'trust-constr':
            options.setdefault('xtol', tol)
            options.setdefault('gtol', tol)
            options.setdefault('barrier_tol', tol)

    if meth == '_custom':
        # custom method called before bounds and constraints are 'standardised'
        # custom method should be able to accept whatever bounds/constraints
        # are provided to it.
        return method(fun, x0, args=args, jac=jac, hess=hess, hessp=hessp,
                      bounds=bounds, constraints=constraints,
                      callback=callback, **options)

    constraints = standardize_constraints(constraints, x0, meth)

    remove_vars = False
    if bounds is not None:
        # convert to new-style bounds so we only have to consider one case
        bounds = standardize_bounds(bounds, x0, 'new')
        bounds = _validate_bounds(bounds, x0, meth)

        if meth in {"tnc", "slsqp", "l-bfgs-b"}:
            # These methods can't take the finite-difference derivatives they
            # need when a variable is fixed by the bounds. To avoid this issue,
            # remove fixed variables from the problem.
            # NOTE: if this list is expanded, then be sure to update the
            # accompanying tests and test_optimize.eb_data. Consider also if
            # default OptimizeResult will need updating.

            # determine whether any variables are fixed
            i_fixed = (bounds.lb == bounds.ub)

            if np.all(i_fixed):
                # all the parameters are fixed, a minimizer is not able to do
                # anything
                return _optimize_result_for_equal_bounds(
                    fun, bounds, meth, args=args, constraints=constraints
                )

            # determine whether finite differences are needed for any grad/jac
            fd_needed = (not callable(jac))
            for con in constraints:
                if not callable(con.get('jac', None)):
                    fd_needed = True

            # If finite differences are ever used, remove all fixed variables
            # Always remove fixed variables for TNC; see gh-14565
            remove_vars = i_fixed.any() and (fd_needed or meth == "tnc")
            if remove_vars:
                x_fixed = (bounds.lb)[i_fixed]
                x0 = x0[~i_fixed]
                bounds = _remove_from_bounds(bounds, i_fixed)
                fun = _Remove_From_Func(fun, i_fixed, x_fixed)

                if callable(callback):
                    sig = wrapped_inspect_signature(callback)
                    if set(sig.parameters) == {'intermediate_result'}:
                        # callback(intermediate_result)
                        print(callback)
                        callback = _Patch_Callback_Equal_Variables(
                            callback, i_fixed, x_fixed
                        )
                    else:
                        # callback(x)
                        callback = _Remove_From_Func(callback, i_fixed, x_fixed)

                if callable(jac):
                    jac = _Remove_From_Func(jac, i_fixed, x_fixed, remove=1)

                # make a copy of the constraints so the user's version doesn't
                # get changed. (Shallow copy is ok)
                constraints = [con.copy() for con in constraints]
                for con in constraints:  # yes, guaranteed to be a list
                    con['fun'] = _Remove_From_Func(con['fun'], i_fixed,
                                                   x_fixed, min_dim=1,
                                                   remove=0)
                    if callable(con.get('jac', None)):
                        con['jac'] = _Remove_From_Func(con['jac'], i_fixed,
                                                       x_fixed, min_dim=2,
                                                       remove=1)
        bounds = standardize_bounds(bounds, x0, meth)

    # selects whether to use callback(x) or callback(intermediate_result)
    callback = _wrap_callback(callback, meth)

    if meth == 'nelder-mead':
        res = _minimize_neldermead(fun, x0, args, callback, bounds=bounds,
                                   **options)
    elif meth == 'powell':
        res = _minimize_powell(fun, x0, args, callback, bounds, **options)
    elif meth == 'cg':
        res = _minimize_cg(fun, x0, args, jac, callback, **options)
    elif meth == 'bfgs':
        res = _minimize_bfgs(fun, x0, args, jac, callback, **options)
    elif meth == 'newton-cg':
        res = _minimize_newtoncg(fun, x0, args, jac, hess, hessp, callback,
                                 **options)
    elif meth == 'l-bfgs-b':
        res = _minimize_lbfgsb(fun, x0, args, jac, bounds,
                               callback=callback, **options)
    elif meth == 'tnc':
        res = _minimize_tnc(fun, x0, args, jac, bounds, callback=callback,
                            **options)
    elif meth == 'cobyla':
        res = _minimize_cobyla(fun, x0, args, constraints, callback=callback,
                               bounds=bounds, **options)
    elif meth == 'cobyqa':
        res = _minimize_cobyqa(fun, x0, args, bounds, constraints, callback,
                               **options)
    elif meth == 'slsqp':
        res = _minimize_slsqp(fun, x0, args, jac, bounds,
                              constraints, callback=callback, **options)
    elif meth == 'trust-constr':
        res = _minimize_trustregion_constr(fun, x0, args, jac, hess, hessp,
                                           bounds, constraints,
                                           callback=callback, **options)
    elif meth == 'dogleg':
        res = _minimize_dogleg(fun, x0, args, jac, hess,
                               callback=callback, **options)
    elif meth == 'trust-ncg':
        res = _minimize_trust_ncg(fun, x0, args, jac, hess, hessp,
                                  callback=callback, **options)
    elif meth == 'trust-krylov':
        res = _minimize_trust_krylov(fun, x0, args, jac, hess, hessp,
                                     callback=callback, **options)
    elif meth == 'trust-exact':
        res = _minimize_trustregion_exact(fun, x0, args, jac, hess,
                                          callback=callback, **options)
    else:
        raise ValueError(f'Unknown solver {method}')

    if remove_vars:
        res.x = _add_to_array(res.x, i_fixed, x_fixed)
        res.jac = _add_to_array(res.jac, i_fixed, np.nan)
        if "hess_inv" in res:
            res.hess_inv = None  # unknown

    if getattr(callback, 'stop_iteration', False):
        res.success = False
        res.status = 99
        res.message = "`callback` raised `StopIteration`."

    return res


def minimize(
    fun,
    x0,
    args=(),
    bounds=None,
    constraints=(),
    callback=None,
    options=None,
    **kwargs,
):
    r"""
    Minimize a scalar function using the COBYQA method.

    The Constrained Optimization BY Quadratic Approximations (COBYQA) method is
    a derivative-free optimization method designed to solve general nonlinear
    optimization problems. A complete description of COBYQA is given in [3]_.

    Parameters
    ----------
    fun : {callable, None}
        Objective function to be minimized.

            ``fun(x, *args) -> float``

        where ``x`` is an array with shape (n,) and `args` is a tuple. If `fun`
        is ``None``, the objective function is assumed to be the zero function,
        resulting in a feasibility problem.
    x0 : array_like, shape (n,)
        Initial guess.
    args : tuple, optional
        Extra arguments passed to the objective function.
    bounds : {`scipy.optimize.Bounds`, array_like, shape (n, 2)}, optional
        Bound constraints of the problem. It can be one of the cases below.

        #. An instance of `scipy.optimize.Bounds`. For the time being, the
           argument ``keep_feasible`` is disregarded, and all the constraints
           are considered unrelaxable and will be enforced.
        #. An array with shape (n, 2). The bound constraints for ``x[i]`` are
           ``bounds[i][0] <= x[i] <= bounds[i][1]``. Set ``bounds[i][0]`` to
           :math:`-\infty` if there is no lower bound, and set ``bounds[i][1]``
           to :math:`\infty` if there is no upper bound.

        The COBYQA method always respect the bound constraints.
    constraints : {Constraint, list}, optional
        General constraints of the problem. It can be one of the cases below.

        #. An instance of `scipy.optimize.LinearConstraint`. The argument
           ``keep_feasible`` is disregarded.
        #. An instance of `scipy.optimize.NonlinearConstraint`. The arguments
           ``jac``, ``hess``, ``keep_feasible``, ``finite_diff_rel_step``, and
           ``finite_diff_jac_sparsity`` are disregarded.

        #. A list, each of whose elements are described in the cases above.

    callback : callable, optional
        A callback executed at each objective function evaluation. The method
        terminates if a ``StopIteration`` exception is raised by the callback
        function. Its signature can be one of the following:

            ``callback(intermediate_result)``

        where ``intermediate_result`` is a keyword parameter that contains an
        instance of `scipy.optimize.OptimizeResult`, with attributes ``x``
        and ``fun``, being the point at which the objective function is
        evaluated and the value of the objective function, respectively. The
        name of the parameter must be ``intermediate_result`` for the callback
        to be passed an instance of `scipy.optimize.OptimizeResult`.

        Alternatively, the callback function can have the signature:

            ``callback(xk)``

        where ``xk`` is the point at which the objective function is evaluated.
        Introspection is used to determine which of the signatures to invoke.
    options : dict, optional
        Options passed to the solver. Accepted keys are:

            disp : bool, optional
                Whether to print information about the optimization procedure.
                Default is ``False``.
            maxfev : int, optional
                Maximum number of function evaluations. Default is ``500 * n``.
            maxiter : int, optional
                Maximum number of iterations. Default is ``1000 * n``.
            target : float, optional
                Target on the objective function value. The optimization
                procedure is terminated when the objective function value of a
                feasible point is less than or equal to this target. Default is
                ``-numpy.inf``.
            feasibility_tol : float, optional
                Tolerance on the constraint violation. If the maximum
                constraint violation at a point is less than or equal to this
                tolerance, the point is considered feasible. Default is
                ``numpy.sqrt(numpy.finfo(float).eps)``.
            radius_init : float, optional
                Initial trust-region radius. Typically, this value should be in
                the order of one tenth of the greatest expected change to `x0`.
                Default is ``1.0``.
            radius_final : float, optional
                Final trust-region radius. It should indicate the accuracy
                required in the final values of the variables. Default is
                ``1e-6``.
            nb_points : int, optional
                Number of interpolation points used to build the quadratic
                models of the objective and constraint functions. Default is
                ``2 * n + 1``.
            scale : bool, optional
                Whether to scale the variables according to the bounds. Default
                is ``False``.
            filter_size : int, optional
                Maximum number of points in the filter. The filter is used to
                select the best point returned by the optimization procedure.
                Default is ``sys.maxsize``.
            store_history : bool, optional
                Whether to store the history of the function evaluations.
                Default is ``False``.
            history_size : int, optional
                Maximum number of function evaluations to store in the history.
                Default is ``sys.maxsize``.
            debug : bool, optional
                Whether to perform additional checks during the optimization
                procedure. This option should be used only for debugging
                purposes and is highly discouraged to general users. Default is
                ``False``.

        Other constants (from the keyword arguments) are described below. They
        are not intended to be changed by general users. They should only be
        changed by users with a deep understanding of the algorithm, who want
        to experiment with different settings.

    Returns
    -------
    `scipy.optimize.OptimizeResult`
        Result of the optimization procedure, with the following fields:

            message : str
                Description of the cause of the termination.
            success : bool
                Whether the optimization procedure terminated successfully.
            status : int
                Termination status of the optimization procedure.
            x : `numpy.ndarray`, shape (n,)
                Solution point.
            fun : float
                Objective function value at the solution point.
            maxcv : float
                Maximum constraint violation at the solution point.
            nfev : int
                Number of function evaluations.
            nit : int
                Number of iterations.

        If ``store_history`` is True, the result also has the following fields:

            fun_history : `numpy.ndarray`, shape (nfev,)
                History of the objective function values.
            maxcv_history : `numpy.ndarray`, shape (nfev,)
                History of the maximum constraint violations.

        A description of the termination statuses is given below.

        .. list-table::
            :widths: 25 75
            :header-rows: 1

            * - Exit status
              - Description
            * - 0
              - The lower bound for the trust-region radius has been reached.
            * - 1
              - The target objective function value has been reached.
            * - 2
              - All variables are fixed by the bound constraints.
            * - 3
              - The callback requested to stop the optimization procedure.
            * - 4
              - The feasibility problem received has been solved successfully.
            * - 5
              - The maximum number of function evaluations has been exceeded.
            * - 6
              - The maximum number of iterations has been exceeded.
            * - -1
              - The bound constraints are infeasible.
            * - -2
              - A linear algebra error occurred.

    Other Parameters
    ----------------
    decrease_radius_factor : float, optional
        Factor by which the trust-region radius is reduced when the reduction
        ratio is low or negative. Default is ``0.5``.
    increase_radius_factor : float, optional
        Factor by which the trust-region radius is increased when the reduction
        ratio is large. Default is ``numpy.sqrt(2.0)``.
    increase_radius_threshold : float, optional
        Threshold that controls the increase of the trust-region radius when
        the reduction ratio is large. Default is ``2.0``.
    decrease_radius_threshold : float, optional
        Threshold used to determine whether the trust-region radius should be
        reduced to the resolution. Default is ``1.4``.
    decrease_resolution_factor : float, optional
        Factor by which the resolution is reduced when the current value is far
        from its final value. Default is ``0.1``.
    large_resolution_threshold : float, optional
        Threshold used to determine whether the resolution is far from its
        final value. Default is ``250.0``.
    moderate_resolution_threshold : float, optional
        Threshold used to determine whether the resolution is close to its
        final value. Default is ``16.0``.
    low_ratio : float, optional
        Threshold used to determine whether the reduction ratio is low. Default
        is ``0.1``.
    high_ratio : float, optional
        Threshold used to determine whether the reduction ratio is high.
        Default is ``0.7``.
    very_low_ratio : float, optional
        Threshold used to determine whether the reduction ratio is very low.
        This is used to determine whether the models should be reset. Default
        is ``0.01``.
    penalty_increase_threshold : float, optional
        Threshold used to determine whether the penalty parameter should be
        increased. Default is ``1.5``.
    penalty_increase_factor : float, optional
        Factor by which the penalty parameter is increased. Default is ``2.0``.
    short_step_threshold : float, optional
        Factor used to determine whether the trial step is too short. Default
        is ``0.5``.
    low_radius_factor : float, optional
        Factor used to determine which interpolation point should be removed
        from the interpolation set at each iteration. Default is ``0.1``.
    byrd_omojokun_factor : float, optional
        Factor by which the trust-region radius is reduced for the computations
        of the normal step in the Byrd-Omojokun composite-step approach.
        Default is ``0.8``.
    threshold_ratio_constraints : float, optional
        Threshold used to determine which constraints should be taken into
        account when decreasing the penalty parameter. Default is ``2.0``.
    large_shift_factor : float, optional
        Factor used to determine whether the point around which the quadratic
        models are built should be updated. Default is ``10.0``.
    large_gradient_factor : float, optional
        Factor used to determine whether the models should be reset. Default is
        ``10.0``.
    resolution_factor : float, optional
        Factor by which the resolution is decreased. Default is ``2.0``.
    improve_tcg : bool, optional
        Whether to improve the steps computed by the truncated conjugate
        gradient method when the trust-region boundary is reached. Default is
        ``True``.

    References
    ----------
    .. [1] J. Nocedal and S. J. Wright. *Numerical Optimization*. Springer Ser.
       Oper. Res. Financ. Eng. Springer, New York, NY, USA, second edition,
       2006. `doi:10.1007/978-0-387-40065-5
       <https://doi.org/10.1007/978-0-387-40065-5>`_.
    .. [2] M. J. D. Powell. A direct search optimization method that models the
       objective and constraint functions by linear interpolation. In S. Gomez
       and J.-P. Hennart, editors, *Advances in Optimization and Numerical
       Analysis*, volume 275 of Math. Appl., pages 51--67. Springer, Dordrecht,
       Netherlands, 1994. `doi:10.1007/978-94-015-8330-5_4
       <https://doi.org/10.1007/978-94-015-8330-5_4>`_.
    .. [3] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.

    Examples
    --------
    To demonstrate how to use `minimize`, we first minimize the Rosenbrock
    function implemented in `scipy.optimize` in an unconstrained setting.

    .. testsetup::

        import numpy as np
        np.set_printoptions(precision=3, suppress=True)

    >>> from cobyqa import minimize
    >>> from scipy.optimize import rosen

    To solve the problem using COBYQA, run:

    >>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
    >>> res = minimize(rosen, x0)
    >>> res.x
    array([1., 1., 1., 1., 1.])

    To see how bound and constraints are handled using `minimize`, we solve
    Example 16.4 of [1]_, defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^2}   & \quad (x_1 - 1)^2 + (x_2 - 2.5)^2\\
            \text{s.t.}                 & \quad -x_1 + 2x_2 \le 2,\\
                                        & \quad x_1 + 2x_2 \le 6,\\
                                        & \quad x_1 - 2x_2 \le 2,\\
                                        & \quad x_1 \ge 0,\\
                                        & \quad x_2 \ge 0.
        \end{aligned}

    >>> import numpy as np
    >>> from scipy.optimize import Bounds, LinearConstraint

    Its objective function can be implemented as:

    >>> def fun(x):
    ...     return (x[0] - 1.0)**2 + (x[1] - 2.5)**2

    This problem can be solved using `minimize` as:

    >>> x0 = [2.0, 0.0]
    >>> bounds = Bounds([0.0, 0.0], np.inf)
    >>> constraints = LinearConstraint([
    ...     [-1.0, 2.0],
    ...     [1.0, 2.0],
    ...     [1.0, -2.0],
    ... ], -np.inf, [2.0, 6.0, 2.0])
    >>> res = minimize(fun, x0, bounds=bounds, constraints=constraints)
    >>> res.x
    array([1.4, 1.7])

    To see how nonlinear constraints are handled, we solve Problem (F) of [2]_,
    defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^2}   & \quad -x_1 - x_2\\
            \text{s.t.}                 & \quad x_1^2 - x_2 \le 0,\\
                                        & \quad x_1^2 + x_2^2 \le 1.
        \end{aligned}

    >>> from scipy.optimize import NonlinearConstraint

    Its objective and constraint functions can be implemented as:

    >>> def fun(x):
    ...     return -x[0] - x[1]
    >>>
    >>> def cub(x):
    ...     return [x[0]**2 - x[1], x[0]**2 + x[1]**2]

    This problem can be solved using `minimize` as:

    >>> x0 = [1.0, 1.0]
    >>> constraints = NonlinearConstraint(cub, -np.inf, [0.0, 1.0])
    >>> res = minimize(fun, x0, constraints=constraints)
    >>> res.x
    array([0.707, 0.707])

    Finally, to see how to supply linear and nonlinear constraints
    simultaneously, we solve Problem (G) of [2]_, defined as

    .. math::

        \begin{aligned}
            \min_{x \in \mathbb{R}^3}   & \quad x_3\\
            \text{s.t.}                 & \quad 5x_1 - x_2 + x_3 \ge 0,\\
                                        & \quad -5x_1 - x_2 + x_3 \ge 0,\\
                                        & \quad x_1^2 + x_2^2 + 4x_2 \le x_3.
        \end{aligned}

    Its objective and nonlinear constraint functions can be implemented as:

    >>> def fun(x):
    ...     return x[2]
    >>>
    >>> def cub(x):
    ...     return x[0]**2 + x[1]**2 + 4.0*x[1] - x[2]

    This problem can be solved using `minimize` as:

    >>> x0 = [1.0, 1.0, 1.0]
    >>> constraints = [
    ...     LinearConstraint(
    ...         [[5.0, -1.0, 1.0], [-5.0, -1.0, 1.0]],
    ...         [0.0, 0.0],
    ...         np.inf,
    ...     ),
    ...     NonlinearConstraint(cub, -np.inf, 0.0),
    ... ]
    >>> res = minimize(fun, x0, constraints=constraints)
    >>> res.x
    array([ 0., -3., -3.])
    """
    # Get basic options that are needed for the initialization.
    if options is None:
        options = {}
    else:
        options = dict(options)
    verbose = options.get(Options.VERBOSE, DEFAULT_OPTIONS[Options.VERBOSE])
    verbose = bool(verbose)
    feasibility_tol = options.get(
        Options.FEASIBILITY_TOL,
        DEFAULT_OPTIONS[Options.FEASIBILITY_TOL],
    )
    feasibility_tol = float(feasibility_tol)
    scale = options.get(Options.SCALE, DEFAULT_OPTIONS[Options.SCALE])
    scale = bool(scale)
    store_history = options.get(
        Options.STORE_HISTORY,
        DEFAULT_OPTIONS[Options.STORE_HISTORY],
    )
    store_history = bool(store_history)
    if Options.HISTORY_SIZE in options and options[Options.HISTORY_SIZE] <= 0:
        raise ValueError("The size of the history must be positive.")
    history_size = options.get(
        Options.HISTORY_SIZE,
        DEFAULT_OPTIONS[Options.HISTORY_SIZE],
    )
    history_size = int(history_size)
    if Options.FILTER_SIZE in options and options[Options.FILTER_SIZE] <= 0:
        raise ValueError("The size of the filter must be positive.")
    filter_size = options.get(
        Options.FILTER_SIZE,
        DEFAULT_OPTIONS[Options.FILTER_SIZE],
    )
    filter_size = int(filter_size)
    debug = options.get(Options.DEBUG, DEFAULT_OPTIONS[Options.DEBUG])
    debug = bool(debug)

    # Initialize the objective function.
    if not isinstance(args, tuple):
        args = (args,)
    obj = ObjectiveFunction(fun, verbose, debug, *args)

    # Initialize the bound constraints.
    if not hasattr(x0, "__len__"):
        x0 = [x0]
    n_orig = len(x0)
    bounds = BoundConstraints(_get_bounds(bounds, n_orig))

    # Initialize the constraints.
    linear_constraints, nonlinear_constraints = _get_constraints(constraints)
    linear = LinearConstraints(linear_constraints, n_orig, debug)
    nonlinear = NonlinearConstraints(nonlinear_constraints, verbose, debug)

    # Initialize the problem (and remove the fixed variables).
    pb = Problem(
        obj,
        x0,
        bounds,
        linear,
        nonlinear,
        callback,
        feasibility_tol,
        scale,
        store_history,
        history_size,
        filter_size,
        debug,
    )

    # Set the default options.
    _set_default_options(options, pb.n)
    constants = _set_default_constants(**kwargs)

    # Initialize the models and skip the computations whenever possible.
    if not pb.bounds.is_feasible:
        # The bound constraints are infeasible.
        return _build_result(
            pb,
            0.0,
            False,
            ExitStatus.INFEASIBLE_ERROR,
            0,
            options,
        )
    elif pb.n == 0:
        # All variables are fixed by the bound constraints.
        return _build_result(
            pb,
            0.0,
            True,
            ExitStatus.FIXED_SUCCESS,
            0,
            options,
        )
    if verbose:
        print("Starting the optimization procedure.")
        print(f"Initial trust-region radius: {options[Options.RHOBEG]}.")
        print(f"Final trust-region radius: {options[Options.RHOEND]}.")
        print(
            f"Maximum number of function evaluations: "
            f"{options[Options.MAX_EVAL]}."
        )
        print(f"Maximum number of iterations: {options[Options.MAX_ITER]}.")
        print()
    try:
        framework = TrustRegion(pb, options, constants)
    except TargetSuccess:
        # The target on the objective function value has been reached
        return _build_result(
            pb,
            0.0,
            True,
            ExitStatus.TARGET_SUCCESS,
            0,
            options,
        )
    except CallbackSuccess:
        # The callback raised a StopIteration exception.
        return _build_result(
            pb,
            0.0,
            True,
            ExitStatus.CALLBACK_SUCCESS,
            0,
            options,
        )
    except FeasibleSuccess:
        # The feasibility problem has been solved successfully.
        return _build_result(
            pb,
            0.0,
            True,
            ExitStatus.FEASIBLE_SUCCESS,
            0,
            options,
        )
    except MaxEvalError:
        # The maximum number of function evaluations has been exceeded.
        return _build_result(
            pb,
            0.0,
            False,
            ExitStatus.MAX_ITER_WARNING,
            0,
            options,
        )
    except np.linalg.LinAlgError:
        # The construction of the initial interpolation set failed.
        return _build_result(
            pb,
            0.0,
            False,
            ExitStatus.LINALG_ERROR,
            0,
            options,
        )

    # Start the optimization procedure.
    success = False
    n_iter = 0
    k_new = None
    n_short_steps = 0
    n_very_short_steps = 0
    n_alt_models = 0
    while True:
        # Stop the optimization procedure if the maximum number of iterations
        # has been exceeded. We do not write the main loop as a for loop
        # because we want to access the number of iterations outside the loop.
        if n_iter >= options[Options.MAX_ITER]:
            status = ExitStatus.MAX_ITER_WARNING
            break
        n_iter += 1

        # Update the point around which the quadratic models are built.
        if (
            np.linalg.norm(
                framework.x_best - framework.models.interpolation.x_base
            )
            >= constants[Constants.LARGE_SHIFT_FACTOR] * framework.radius
        ):
            framework.shift_x_base(options)

        # Evaluate the trial step.
        radius_save = framework.radius
        normal_step, tangential_step = framework.get_trust_region_step(options)
        step = normal_step + tangential_step
        s_norm = np.linalg.norm(step)

        # If the trial step is too short, we do not attempt to evaluate the
        # objective and constraint functions. Instead, we reduce the
        # trust-region radius and check whether the resolution should be
        # enhanced and whether the geometry of the interpolation set should be
        # improved. Otherwise, we entertain a classical iteration. The
        # criterion for performing an exceptional jump is taken from NEWUOA.
        if (
            s_norm
            <= constants[Constants.SHORT_STEP_THRESHOLD] * framework.resolution
        ):
            framework.radius *= constants[Constants.DECREASE_RESOLUTION_FACTOR]
            if radius_save > framework.resolution:
                n_short_steps = 0
                n_very_short_steps = 0
            else:
                n_short_steps += 1
                n_very_short_steps += 1
                if s_norm > 0.1 * framework.resolution:
                    n_very_short_steps = 0
            enhance_resolution = n_short_steps >= 5 or n_very_short_steps >= 3
            if enhance_resolution:
                n_short_steps = 0
                n_very_short_steps = 0
                improve_geometry = False
            else:
                try:
                    k_new, dist_new = framework.get_index_to_remove()
                except np.linalg.LinAlgError:
                    status = ExitStatus.LINALG_ERROR
                    break
                improve_geometry = dist_new > max(
                    framework.radius,
                    constants[Constants.RESOLUTION_FACTOR]
                    * framework.resolution,
                )
        else:
            # Increase the penalty parameter if necessary.
            same_best_point = framework.increase_penalty(step)
            if same_best_point:
                # Evaluate the objective and constraint functions.
                try:
                    fun_val, cub_val, ceq_val = _eval(
                        pb,
                        framework,
                        step,
                        options,
                    )
                except TargetSuccess:
                    status = ExitStatus.TARGET_SUCCESS
                    success = True
                    break
                except FeasibleSuccess:
                    status = ExitStatus.FEASIBLE_SUCCESS
                    success = True
                    break
                except CallbackSuccess:
                    status = ExitStatus.CALLBACK_SUCCESS
                    success = True
                    break
                except MaxEvalError:
                    status = ExitStatus.MAX_EVAL_WARNING
                    break

                # Perform a second-order correction step if necessary.
                merit_old = framework.merit(
                    framework.x_best,
                    framework.fun_best,
                    framework.cub_best,
                    framework.ceq_best,
                )
                merit_new = framework.merit(
                    framework.x_best + step, fun_val, cub_val, ceq_val
                )
                if (
                    pb.type == "nonlinearly constrained"
                    and merit_new > merit_old
                    and np.linalg.norm(normal_step)
                    > constants[Constants.BYRD_OMOJOKUN_FACTOR] ** 2.0
                    * framework.radius
                ):
                    soc_step = framework.get_second_order_correction_step(
                        step, options
                    )
                    if np.linalg.norm(soc_step) > 0.0:
                        step += soc_step

                        # Evaluate the objective and constraint functions.
                        try:
                            fun_val, cub_val, ceq_val = _eval(
                                pb,
                                framework,
                                step,
                                options,
                            )
                        except TargetSuccess:
                            status = ExitStatus.TARGET_SUCCESS
                            success = True
                            break
                        except FeasibleSuccess:
                            status = ExitStatus.FEASIBLE_SUCCESS
                            success = True
                            break
                        except CallbackSuccess:
                            status = ExitStatus.CALLBACK_SUCCESS
                            success = True
                            break
                        except MaxEvalError:
                            status = ExitStatus.MAX_EVAL_WARNING
                            break

                # Calculate the reduction ratio.
                ratio = framework.get_reduction_ratio(
                    step,
                    fun_val,
                    cub_val,
                    ceq_val,
                )

                # Choose an interpolation point to remove.
                try:
                    k_new = framework.get_index_to_remove(
                        framework.x_best + step
                    )[0]
                except np.linalg.LinAlgError:
                    status = ExitStatus.LINALG_ERROR
                    break

                # Update the interpolation set.
                try:
                    ill_conditioned = framework.models.update_interpolation(
                        k_new, framework.x_best + step, fun_val, cub_val,
                        ceq_val
                    )
                except np.linalg.LinAlgError:
                    status = ExitStatus.LINALG_ERROR
                    break
                framework.set_best_index()

                # Update the trust-region radius.
                framework.update_radius(step, ratio)

                # Attempt to replace the models by the alternative ones.
                if framework.radius <= framework.resolution:
                    if ratio >= constants[Constants.VERY_LOW_RATIO]:
                        n_alt_models = 0
                    else:
                        n_alt_models += 1
                        grad = framework.models.fun_grad(framework.x_best)
                        try:
                            grad_alt = framework.models.fun_alt_grad(
                                framework.x_best
                            )
                        except np.linalg.LinAlgError:
                            status = ExitStatus.LINALG_ERROR
                            break
                        if np.linalg.norm(grad) < constants[
                            Constants.LARGE_GRADIENT_FACTOR
                        ] * np.linalg.norm(grad_alt):
                            n_alt_models = 0
                        if n_alt_models >= 3:
                            try:
                                framework.models.reset_models()
                            except np.linalg.LinAlgError:
                                status = ExitStatus.LINALG_ERROR
                                break
                            n_alt_models = 0

                # Update the Lagrange multipliers.
                framework.set_multipliers(framework.x_best + step)

                # Check whether the resolution should be enhanced.
                try:
                    k_new, dist_new = framework.get_index_to_remove()
                except np.linalg.LinAlgError:
                    status = ExitStatus.LINALG_ERROR
                    break
                improve_geometry = (
                    ill_conditioned
                    or ratio <= constants[Constants.LOW_RATIO]
                    and dist_new
                    > max(
                        framework.radius,
                        constants[Constants.RESOLUTION_FACTOR]
                        * framework.resolution,
                    )
                )
                enhance_resolution = (
                    radius_save <= framework.resolution
                    and ratio <= constants[Constants.LOW_RATIO]
                    and not improve_geometry
                )
            else:
                # When increasing the penalty parameter, the best point so far
                # may change. In this case, we restart the iteration.
                enhance_resolution = False
                improve_geometry = False

        # Reduce the resolution if necessary.
        if enhance_resolution:
            if framework.resolution <= options[Options.RHOEND]:
                success = True
                status = ExitStatus.RADIUS_SUCCESS
                break
            framework.enhance_resolution(options)
            framework.decrease_penalty()

            if verbose:
                maxcv_val = pb.maxcv(
                    framework.x_best, framework.cub_best, framework.ceq_best
                )
                _print_step(
                    f"New trust-region radius: {framework.resolution}",
                    pb,
                    pb.build_x(framework.x_best),
                    framework.fun_best,
                    maxcv_val,
                    pb.n_eval,
                    n_iter,
                )
                print()

        # Improve the geometry of the interpolation set if necessary.
        if improve_geometry:
            try:
                step = framework.get_geometry_step(k_new, options)
            except np.linalg.LinAlgError:
                status = ExitStatus.LINALG_ERROR
                break

            # Evaluate the objective and constraint functions.
            try:
                fun_val, cub_val, ceq_val = _eval(pb, framework, step, options)
            except TargetSuccess:
                status = ExitStatus.TARGET_SUCCESS
                success = True
                break
            except FeasibleSuccess:
                status = ExitStatus.FEASIBLE_SUCCESS
                success = True
                break
            except CallbackSuccess:
                status = ExitStatus.CALLBACK_SUCCESS
                success = True
                break
            except MaxEvalError:
                status = ExitStatus.MAX_EVAL_WARNING
                break

            # Update the interpolation set.
            try:
                framework.models.update_interpolation(
                    k_new,
                    framework.x_best + step,
                    fun_val,
                    cub_val,
                    ceq_val,
                )
            except np.linalg.LinAlgError:
                status = ExitStatus.LINALG_ERROR
                break
            framework.set_best_index()

    return _build_result(
        pb,
        framework.penalty,
        success,
        status,
        n_iter,
        options,
    )


def minimize(fun, x0, args=(), method=None, bounds=None, constraints=(), callback=None, options=None):

    linear_constraint, nonlinear_constraint_function = process_constraints(constraints)

    options = {'quiet': True} if options is None else options
    quiet = options.get("quiet", True)

    if method is None:
        if nonlinear_constraint_function is not None:
            if not quiet: print("Nonlinear constraints detected, applying COBYLA")
            method = "cobyla"
        elif linear_constraint is not None:
            if not quiet: print("Linear constraints detected without nonlinear constraints, applying LINCOA")
            method = "lincoa"
        elif bounds is not None:
            if not quiet: print("Bounds without linear or nonlinear constraints detected, applying BOBYQA")
            method = "bobyqa"
        else:
            if not quiet: print("No bounds or constraints detected, applying NEWUOA")
            method = "newuoa"
    else:
        # Raise some errors if methods were called with inappropriate options
        method = method.lower()
        if method not in ('newuoa', 'uobyqa', 'bobyqa', 'cobyla', 'lincoa'):
            raise ValueError(f"Method must be one of NEWUOA, UOBYQA, BOBYQA, COBYLA, or LINCOA, not '{method}'")
        if method != "cobyla" and nonlinear_constraint_function is not None:
            raise ValueError("Nonlinear constraints were provided for an algorithm that cannot handle them")
        if method not in ("cobyla", "lincoa") and linear_constraint is not None:
            raise ValueError("Linear constraints were provided for an algorithm that cannot handle them")
        if method not in ("cobyla", "bobyqa", "lincoa") and bounds is not None:
            raise ValueError("Bounds were provided for an algorithm that cannot handle them")

    # Try to get the length of x0. If we can't that likely means it's a scalar, and
    # in that case we turn it into an array and wrap the original function so that it
    # can accept an array and return a scalar.
    try:
        lenx0 = len(x0)
    except TypeError:
        x0 = np.array([x0])
        original_scalar_fun = fun
        def scalar_fun(x):
            return original_scalar_fun(x[0], *args)
        fun = scalar_fun
        lenx0 = 1

    lb, ub = process_bounds(bounds, lenx0)

    # Check which variables are fixed and eliminate them from the problem.
    # Save the indices and values so that we can call the original function with
    # an array of the appropriate size, and so that we can add the fixed values to the
    # result when COBYLA returns.
    tol = get_arrays_tol(lb, ub)
    _fixed_idx = (
        (lb <= ub)
        & (np.abs(lb - ub) < tol)
    )
    if any(_fixed_idx):
        _fixed_values = 0.5 * (
            lb[_fixed_idx] + ub[_fixed_idx]
        )
        _fixed_values = np.clip(
            _fixed_values,
            lb[_fixed_idx],
            ub[_fixed_idx],
        )
        x0 = x0[~_fixed_idx]
        lb = lb[~_fixed_idx]
        ub = ub[~_fixed_idx]
        original_fun = fun
        def fixed_fun(x):
            newx = np.zeros(lenx0)
            newx[_fixed_idx] = _fixed_values
            newx[~_fixed_idx] = x
            return original_fun(newx, *args)
        fun = fixed_fun


    # Project x0 onto the feasible set
    if nonlinear_constraint_function is None:
        result = _project(x0, lb, ub, {"linear": linear_constraint, "nonlinear": None})
        x0 = result.x
    
    if linear_constraint is not None:
        A_eq, b_eq, A_ineq, b_ineq = separate_LC_into_eq_and_ineq(linear_constraint)
    else:
        A_eq, b_eq, A_ineq, b_ineq = None, None, None, None

    if nonlinear_constraint_function is not None:
        # If there is a nonlinear constraint function, we will call COBYLA, which needs the number of nonlinear
        # constraints (m_nlcon). In order to get this number we need to evaluate the constraint function at x0.
        # The constraint value at x0 (nlconstr0) is not discarded but passed down to the Fortran backend, as its
        # evaluation is assumed to be expensive. We also evaluate the objective function at x0 and pass the result
        # (f0) down to the Fortran backend, which expects nlconstr0 and f0 to be provided in sync.
        def calcfc(x):
            f = fun(x, *args)
            nlconstr = nonlinear_constraint_function(x)
            return f, nlconstr
    else:
        def calcfc(x):
            f = fun(x, *args)
            constr = np.zeros(0)
            return f, constr

    f0, nlconstr0 = calcfc(x0)

    if 'quiet' in options:
        del options['quiet']

    if 'maxfev' in options:
        options['maxfun'] = options['maxfev']
        del options['maxfev']

    result = cobyla(
        calcfc,
        len(nlconstr0),
        x0,
        A_ineq,
        b_ineq,
        A_eq,
        b_eq,
        lb,
        ub,
        f0=f0,
        nlconstr0=nlconstr0,
        callback=callback,
        **options
    )

    if any(_fixed_idx):
        newx = np.zeros(lenx0)
        newx[_fixed_idx] = _fixed_values
        newx[~_fixed_idx] = result.x
        result.x = newx
    return result


def minimize(
    fun: Callable,
    x0: Array,
    args: tuple = (),
    *,
    method: str,
    tol: float | None = None,
    options: Mapping[str, Any] | None = None,
) -> OptimizeResults:
  """Minimization of scalar function of one or more variables.

  This API for this function matches SciPy with some minor deviations:

  - Gradients of ``fun`` are calculated automatically using JAX's autodiff
    support when required.
  - The ``method`` argument is required. You must specify a solver.
  - Various optional arguments in the SciPy interface have not yet been
    implemented.
  - Optimization results may differ from SciPy due to differences in the line
    search implementation.

  ``minimize`` supports :func:`~jax.jit` compilation. It does not yet support
  differentiation or arguments in the form of multi-dimensional arrays, but
  support for both is planned.

  Args:
    fun: the objective function to be minimized, ``fun(x, *args) -> float``,
      where ``x`` is a 1-D array with shape ``(n,)`` and ``args`` is a tuple
      of the fixed parameters needed to completely specify the function.
      ``fun`` must support differentiation.
    x0: initial guess. Array of real elements of size ``(n,)``, where ``n`` is
      the number of independent variables.
    args: extra arguments passed to the objective function.
    method: solver type. Currently only ``"BFGS"`` is supported.
    tol: tolerance for termination. For detailed control, use solver-specific
      options.
    options: a dictionary of solver options. All methods accept the following
      generic options:

      - maxiter (int): Maximum number of iterations to perform. Depending on the
        method each iteration may use several function evaluations.

  Returns:
    An :class:`OptimizeResults` object.
  """
  if options is None:
    options = {}

  if not isinstance(args, tuple):
    msg = "args argument to jax.scipy.optimize.minimize must be a tuple, got {}"
    raise TypeError(msg.format(args))

  fun_with_args = lambda x: fun(x, *args)

  if method.lower() == 'bfgs':
    results = minimize_bfgs(fun_with_args, x0, **options)
    success = results.converged & jnp.logical_not(results.failed)
    return OptimizeResults(x=results.x_k,
                           success=success,
                           status=results.status,
                           fun=results.f_k,
                           jac=results.g_k,
                           hess_inv=results.H_k,
                           nfev=results.nfev,
                           njev=results.ngev,
                           nit=results.k)

  if method.lower() == 'l-bfgs-experimental-do-not-rely-on-this':
    results = _minimize_lbfgs(fun_with_args, x0, **options)
    success = results.converged & jnp.logical_not(results.failed)
    return OptimizeResults(x=results.x_k,
                           success=success,
                           status=results.status,
                           fun=results.f_k,
                           jac=results.g_k,
                           hess_inv=None,
                           nfev=results.nfev,
                           njev=results.ngev,
                           nit=results.k)

  raise ValueError(f"Method {method} not recognized")

