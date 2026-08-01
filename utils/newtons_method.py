
def newtons_method(expr, wrt, atol=1e-12, delta=None, *, rtol=4e-16, debug=False,
                   itermax=None, counter=None, delta_fn=lambda e, x: -e/e.diff(x),
                   cse=False, handle_nan=None,
                   bounds=None):
    """ Generates an AST for Newton-Raphson method (a root-finding algorithm).

    Explanation
    ===========

    Returns an abstract syntax tree (AST) based on ``sympy.codegen.ast`` for Netwon's
    method of root-finding.

    Parameters
    ==========

    expr : expression
    wrt : Symbol
        With respect to, i.e. what is the variable.
    atol : number or expression
        Absolute tolerance (stopping criterion)
    rtol : number or expression
        Relative tolerance (stopping criterion)
    delta : Symbol
        Will be a ``Dummy`` if ``None``.
    debug : bool
        Whether to print convergence information during iterations
    itermax : number or expr
        Maximum number of iterations.
    counter : Symbol
        Will be a ``Dummy`` if ``None``.
    delta_fn: Callable[[Expr, Symbol], Expr]
        computes the step, default is newtons method. For e.g. Halley's method
        use delta_fn=lambda e, x: -2*e*e.diff(x)/(2*e.diff(x)**2 - e*e.diff(x, 2))
    cse: bool
        Perform common sub-expression elimination on delta expression
    handle_nan: Token
        How to handle occurrence of not-a-number (NaN).
    bounds: Optional[tuple[Expr, Expr]]
        Perform optimization within bounds

    Examples
    ========

    >>> from sympy import symbols, cos
    >>> from sympy.codegen.ast import Assignment
    >>> from sympy.codegen.algorithms import newtons_method
    >>> x, dx, atol = symbols('x dx atol')
    >>> expr = cos(x) - x**3
    >>> algo = newtons_method(expr, x, atol=atol, delta=dx)
    >>> algo.has(Assignment(dx, -expr/expr.diff(x)))
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Newton%27s_method

    """

    if delta is None:
        delta = Dummy()
        Wrapper = Scope
        name_d = 'delta'
    else:
        Wrapper = lambda x: x
        name_d = delta.name

    delta_expr = delta_fn(expr, wrt)
    if cse:
        from sympy.simplify.cse_main import cse
        cses, (red,) = cse([delta_expr.factor()])
        whl_bdy = [Assignment(dum, sub_e) for dum, sub_e in cses]
        whl_bdy += [Assignment(delta, red)]
    else:
        whl_bdy = [Assignment(delta, delta_expr)]
    if handle_nan is not None:
        whl_bdy += [While(isnan(delta), CodeBlock(handle_nan, break_))]
    whl_bdy += [AddAugmentedAssignment(wrt, delta)]
    if bounds is not None:
        whl_bdy += [Assignment(wrt, Min(Max(wrt, bounds[0]), bounds[1]))]
    if debug:
        prnt = Print([wrt, delta], r"{}=%12.5g {}=%12.5g\n".format(wrt.name, name_d))
        whl_bdy += [prnt]
    req = Gt(Abs(delta), atol + rtol*Abs(wrt))
    declars = [Declaration(Variable(delta, type=real, value=oo))]
    if itermax is not None:
        counter = counter or Dummy(integer=True)
        v_counter = Variable.deduced(counter, 0)
        declars.append(Declaration(v_counter))
        whl_bdy.append(AddAugmentedAssignment(counter, 1))
        req = And(req, Lt(counter, itermax))
    whl = While(req, CodeBlock(*whl_bdy))
    blck = declars
    if debug:
        blck.append(Print([wrt], r"{}=%12.5g\n".format(wrt.name)))
    blck += [whl]
    return Wrapper(CodeBlock(*blck))

