
def solve(input: Tensor, A: Tensor, *, out=None) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.solve` is deprecated in favor of `torch.linalg.solve`. "
        "`torch.linalg.solve` has its arguments reversed and does not return the LU factorization.\n\n"
        "To get the LU factorization see `torch.lu`, which can be used with `torch.lu_solve` or `torch.lu_unpack`.\n"
        "X = torch.solve(B, A).solution "
        "should be replaced with:\n"
        "X = torch.linalg.solve(A, B)"
    )


def solve(a: ArrayLike, b: ArrayLike):
    a, b = _atleast_float_2(a, b)
    return torch.linalg.solve(a, b)


def solve(f, *symbols, **flags):
    r"""
    Algebraically solves equations and systems of equations.

    Explanation
    ===========

    Currently supported:
        - polynomial
        - transcendental
        - piecewise combinations of the above
        - systems of linear and polynomial equations
        - systems containing relational expressions
        - systems implied by undetermined coefficients

    Examples
    ========

    The default output varies according to the input and might
    be a list (possibly empty), a dictionary, a list of
    dictionaries or tuples, or an expression involving relationals.
    For specifics regarding different forms of output that may appear, see :ref:`solve_output`.
    Let it suffice here to say that to obtain a uniform output from
    `solve` use ``dict=True`` or ``set=True`` (see below).

        >>> from sympy import solve, Poly, Eq, Matrix, Symbol
        >>> from sympy.abc import x, y, z, a, b

    The expressions that are passed can be Expr, Equality, or Poly
    classes (or lists of the same); a Matrix is considered to be a
    list of all the elements of the matrix:

        >>> solve(x - 3, x)
        [3]
        >>> solve(Eq(x, 3), x)
        [3]
        >>> solve(Poly(x - 3), x)
        [3]
        >>> solve(Matrix([[x, x + y]]), x, y) == solve([x, x + y], x, y)
        True

    If no symbols are indicated to be of interest and the equation is
    univariate, a list of values is returned; otherwise, the keys in
    a dictionary will indicate which (of all the variables used in
    the expression(s)) variables and solutions were found:

        >>> solve(x**2 - 4)
        [-2, 2]
        >>> solve((x - a)*(y - b))
        [{a: x}, {b: y}]
        >>> solve([x - 3, y - 1])
        {x: 3, y: 1}
        >>> solve([x - 3, y**2 - 1])
        [{x: 3, y: -1}, {x: 3, y: 1}]

    If you pass symbols for which solutions are sought, the output will vary
    depending on the number of symbols you passed, whether you are passing
    a list of expressions or not, and whether a linear system was solved.
    Uniform output is attained by using ``dict=True`` or ``set=True``.

        >>> #### *** feel free to skip to the stars below *** ####
        >>> from sympy import TableForm
        >>> h = [None, ';|;'.join(['e', 's', 'solve(e, s)', 'solve(e, s, dict=True)',
        ... 'solve(e, s, set=True)']).split(';')]
        >>> t = []
        >>> for e, s in [
        ...         (x - y, y),
        ...         (x - y, [x, y]),
        ...         (x**2 - y, [x, y]),
        ...         ([x - 3, y -1], [x, y]),
        ...         ]:
        ...     how = [{}, dict(dict=True), dict(set=True)]
        ...     res = [solve(e, s, **f) for f in how]
        ...     t.append([e, '|', s, '|'] + [res[0], '|', res[1], '|', res[2]])
        ...
        >>> # ******************************************************* #
        >>> TableForm(t, headings=h, alignments="<")
        e              | s      | solve(e, s)  | solve(e, s, dict=True) | solve(e, s, set=True)
        ---------------------------------------------------------------------------------------
        x - y          | y      | [x]          | [{y: x}]               | ([y], {(x,)})
        x - y          | [x, y] | [(y, y)]     | [{x: y}]               | ([x, y], {(y, y)})
        x**2 - y       | [x, y] | [(x, x**2)]  | [{y: x**2}]            | ([x, y], {(x, x**2)})
        [x - 3, y - 1] | [x, y] | {x: 3, y: 1} | [{x: 3, y: 1}]         | ([x, y], {(3, 1)})

        * If any equation does not depend on the symbol(s) given, it will be
          eliminated from the equation set and an answer may be given
          implicitly in terms of variables that were not of interest:

            >>> solve([x - y, y - 3], x)
            {x: y}

    When you pass all but one of the free symbols, an attempt
    is made to find a single solution based on the method of
    undetermined coefficients. If it succeeds, a dictionary of values
    is returned. If you want an algebraic solutions for one
    or more of the symbols, pass the expression to be solved in a list:

        >>> e = a*x + b - 2*x - 3
        >>> solve(e, [a, b])
        {a: 2, b: 3}
        >>> solve([e], [a, b])
        {a: -b/x + (2*x + 3)/x}

    When there is no solution for any given symbol which will make all
    expressions zero, the empty list is returned (or an empty set in
    the tuple when ``set=True``):

        >>> from sympy import sqrt
        >>> solve(3, x)
        []
        >>> solve(x - 3, y)
        []
        >>> solve(sqrt(x) + 1, x, set=True)
        ([x], set())

    When an object other than a Symbol is given as a symbol, it is
    isolated algebraically and an implicit solution may be obtained.
    This is mostly provided as a convenience to save you from replacing
    the object with a Symbol and solving for that Symbol. It will only
    work if the specified object can be replaced with a Symbol using the
    subs method:

        >>> from sympy import exp, Function
        >>> f = Function('f')

        >>> solve(f(x) - x, f(x))
        [x]
        >>> solve(f(x).diff(x) - f(x) - x, f(x).diff(x))
        [x + f(x)]
        >>> solve(f(x).diff(x) - f(x) - x, f(x))
        [-x + Derivative(f(x), x)]
        >>> solve(x + exp(x)**2, exp(x), set=True)
        ([exp(x)], {(-sqrt(-x),), (sqrt(-x),)})

        >>> from sympy import Indexed, IndexedBase, Tuple
        >>> A = IndexedBase('A')
        >>> eqs = Tuple(A[1] + A[2] - 3, A[1] - A[2] + 1)
        >>> solve(eqs, eqs.atoms(Indexed))
        {A[1]: 1, A[2]: 2}

        * To solve for a function within a derivative, use :func:`~.dsolve`.

    To solve for a symbol implicitly, use implicit=True:

        >>> solve(x + exp(x), x)
        [-LambertW(1)]
        >>> solve(x + exp(x), x, implicit=True)
        [-exp(x)]

    It is possible to solve for anything in an expression that can be
    replaced with a symbol using :obj:`~sympy.core.basic.Basic.subs`:

        >>> solve(x + 2 + sqrt(3), x + 2)
        [-sqrt(3)]
        >>> solve((x + 2 + sqrt(3), x + 4 + y), y, x + 2)
        {y: -2 + sqrt(3), x + 2: -sqrt(3)}

        * Nothing heroic is done in this implicit solving so you may end up
          with a symbol still in the solution:

            >>> eqs = (x*y + 3*y + sqrt(3), x + 4 + y)
            >>> solve(eqs, y, x + 2)
            {y: -sqrt(3)/(x + 3), x + 2: -2*x/(x + 3) - 6/(x + 3) + sqrt(3)/(x + 3)}
            >>> solve(eqs, y*x, x)
            {x: -y - 4, x*y: -3*y - sqrt(3)}

        * If you attempt to solve for a number, remember that the number
          you have obtained does not necessarily mean that the value is
          equivalent to the expression obtained:

            >>> solve(sqrt(2) - 1, 1)
            [sqrt(2)]
            >>> solve(x - y + 1, 1)  # /!\ -1 is targeted, too
            [x/(y - 1)]
            >>> [_.subs(z, -1) for _ in solve((x - y + 1).subs(-1, z), 1)]
            [-x + y]

    **Additional Examples**

    ``solve()`` with check=True (default) will run through the symbol tags to
    eliminate unwanted solutions. If no assumptions are included, all possible
    solutions will be returned:

        >>> x = Symbol("x")
        >>> solve(x**2 - 1)
        [-1, 1]

    By setting the ``positive`` flag, only one solution will be returned:

        >>> pos = Symbol("pos", positive=True)
        >>> solve(pos**2 - 1)
        [1]

    When the solutions are checked, those that make any denominator zero
    are automatically excluded. If you do not want to exclude such solutions,
    then use the check=False option:

        >>> from sympy import sin, limit
        >>> solve(sin(x)/x)  # 0 is excluded
        [pi]

    If ``check=False``, then a solution to the numerator being zero is found
    but the value of $x = 0$ is a spurious solution since $\sin(x)/x$ has the well
    known limit (without discontinuity) of 1 at $x = 0$:

        >>> solve(sin(x)/x, check=False)
        [0, pi]

    In the following case, however, the limit exists and is equal to the
    value of $x = 0$ that is excluded when check=True:

        >>> eq = x**2*(1/x - z**2/x)
        >>> solve(eq, x)
        []
        >>> solve(eq, x, check=False)
        [0]
        >>> limit(eq, x, 0, '-')
        0
        >>> limit(eq, x, 0, '+')
        0

    **Solving Relationships**

    When one or more expressions passed to ``solve`` is a relational,
    a relational result is returned (and the ``dict`` and ``set`` flags
    are ignored):

        >>> solve(x < 3)
        (-oo < x) & (x < 3)
        >>> solve([x < 3, x**2 > 4], x)
        ((-oo < x) & (x < -2)) | ((2 < x) & (x < 3))
        >>> solve([x + y - 3, x > 3], x)
        (3 < x) & (x < oo) & Eq(x, 3 - y)

    Although checking of assumptions on symbols in relationals
    is not done, setting assumptions will affect how certain
    relationals might automatically simplify:

        >>> solve(x**2 > 4)
        ((-oo < x) & (x < -2)) | ((2 < x) & (x < oo))

        >>> r = Symbol('r', real=True)
        >>> solve(r**2 > 4)
        (2 < r) | (r < -2)

    There is currently no algorithm in SymPy that allows you to use
    relationships to resolve more than one variable. So the following
    does not determine that ``q < 0`` (and trying to solve for ``r``
    and ``q`` will raise an error):

        >>> from sympy import symbols
        >>> r, q = symbols('r, q', real=True)
        >>> solve([r + q - 3, r > 3], r)
        (3 < r) & Eq(r, 3 - q)

    You can directly call the routine that ``solve`` calls
    when it encounters a relational: :func:`~.reduce_inequalities`.
    It treats Expr like Equality.

        >>> from sympy import reduce_inequalities
        >>> reduce_inequalities([x**2 - 4])
        Eq(x, -2) | Eq(x, 2)

    If each relationship contains only one symbol of interest,
    the expressions can be processed for multiple symbols:

        >>> reduce_inequalities([0 <= x  - 1, y < 3], [x, y])
        (-oo < y) & (1 <= x) & (x < oo) & (y < 3)

    But an error is raised if any relationship has more than one
    symbol of interest:

        >>> reduce_inequalities([0 <= x*y  - 1, y < 3], [x, y])
        Traceback (most recent call last):
        ...
        NotImplementedError:
        inequality has more than one symbol of interest.

    **Disabling High-Order Explicit Solutions**

    When solving polynomial expressions, you might not want explicit solutions
    (which can be quite long). If the expression is univariate, ``CRootOf``
    instances will be returned instead:

        >>> solve(x**3 - x + 1)
        [-1/((-1/2 - sqrt(3)*I/2)*(3*sqrt(69)/2 + 27/2)**(1/3)) -
        (-1/2 - sqrt(3)*I/2)*(3*sqrt(69)/2 + 27/2)**(1/3)/3,
        -(-1/2 + sqrt(3)*I/2)*(3*sqrt(69)/2 + 27/2)**(1/3)/3 -
        1/((-1/2 + sqrt(3)*I/2)*(3*sqrt(69)/2 + 27/2)**(1/3)),
        -(3*sqrt(69)/2 + 27/2)**(1/3)/3 -
        1/(3*sqrt(69)/2 + 27/2)**(1/3)]
        >>> solve(x**3 - x + 1, cubics=False)
        [CRootOf(x**3 - x + 1, 0),
         CRootOf(x**3 - x + 1, 1),
         CRootOf(x**3 - x + 1, 2)]

    If the expression is multivariate, no solution might be returned:

        >>> solve(x**3 - x + a, x, cubics=False)
        []

    Sometimes solutions will be obtained even when a flag is False because the
    expression could be factored. In the following example, the equation can
    be factored as the product of a linear and a quadratic factor so explicit
    solutions (which did not require solving a cubic expression) are obtained:

        >>> eq = x**3 + 3*x**2 + x - 1
        >>> solve(eq, cubics=False)
        [-1, -1 + sqrt(2), -sqrt(2) - 1]

    **Solving Equations Involving Radicals**

    Because of SymPy's use of the principle root, some solutions
    to radical equations will be missed unless check=False:

        >>> from sympy import root
        >>> eq = root(x**3 - 3*x**2, 3) + 1 - x
        >>> solve(eq)
        []
        >>> solve(eq, check=False)
        [1/3]

    In the above example, there is only a single solution to the
    equation. Other expressions will yield spurious roots which
    must be checked manually; roots which give a negative argument
    to odd-powered radicals will also need special checking:

        >>> from sympy import real_root, S
        >>> eq = root(x, 3) - root(x, 5) + S(1)/7
        >>> solve(eq)  # this gives 2 solutions but misses a 3rd
        [CRootOf(7*x**5 - 7*x**3 + 1, 1)**15,
        CRootOf(7*x**5 - 7*x**3 + 1, 2)**15]
        >>> sol = solve(eq, check=False)
        >>> [abs(eq.subs(x,i).n(2)) for i in sol]
        [0.48, 0.e-110, 0.e-110, 0.052, 0.052]

    The first solution is negative so ``real_root`` must be used to see that it
    satisfies the expression:

        >>> abs(real_root(eq.subs(x, sol[0])).n(2))
        0.e-110

    If the roots of the equation are not real then more care will be
    necessary to find the roots, especially for higher order equations.
    Consider the following expression:

        >>> expr = root(x, 3) - root(x, 5)

    We will construct a known value for this expression at x = 3 by selecting
    the 1-th root for each radical:

        >>> expr1 = root(x, 3, 1) - root(x, 5, 1)
        >>> v = expr1.subs(x, -3)

    The ``solve`` function is unable to find any exact roots to this equation:

        >>> eq = Eq(expr, v); eq1 = Eq(expr1, v)
        >>> solve(eq, check=False), solve(eq1, check=False)
        ([], [])

    The function ``unrad``, however, can be used to get a form of the equation
    for which numerical roots can be found:

        >>> from sympy.solvers.solvers import unrad
        >>> from sympy import nroots
        >>> e, (p, cov) = unrad(eq)
        >>> pvals = nroots(e)
        >>> inversion = solve(cov, x)[0]
        >>> xvals = [inversion.subs(p, i) for i in pvals]

    Although ``eq`` or ``eq1`` could have been used to find ``xvals``, the
    solution can only be verified with ``expr1``:

        >>> z = expr - v
        >>> [xi.n(chop=1e-9) for xi in xvals if abs(z.subs(x, xi).n()) < 1e-9]
        []
        >>> z1 = expr1 - v
        >>> [xi.n(chop=1e-9) for xi in xvals if abs(z1.subs(x, xi).n()) < 1e-9]
        [-3.0]

    Parameters
    ==========

    f :
        - a single Expr or Poly that must be zero
        - an Equality
        - a Relational expression
        - a Boolean
        - iterable of one or more of the above

    symbols : (object(s) to solve for) specified as
        - none given (other non-numeric objects will be used)
        - single symbol
        - denested list of symbols
          (e.g., ``solve(f, x, y)``)
        - ordered iterable of symbols
          (e.g., ``solve(f, [x, y])``)

    flags :
        dict=True (default is False)
            Return list (perhaps empty) of solution mappings.
        set=True (default is False)
            Return list of symbols and set of tuple(s) of solution(s).
        exclude=[] (default)
            Do not try to solve for any of the free symbols in exclude;
            if expressions are given, the free symbols in them will
            be extracted automatically.
        check=True (default)
            If False, do not do any testing of solutions. This can be
            useful if you want to include solutions that make any
            denominator zero.
        numerical=True (default)
            Do a fast numerical check if *f* has only one symbol.
        minimal=True (default is False)
            A very fast, minimal testing.
        warn=True (default is False)
            Show a warning if ``checksol()`` could not conclude.
        simplify=True (default)
            Simplify all but polynomials of order 3 or greater before
            returning them and (if check is not False) use the
            general simplify function on the solutions and the
            expression obtained when they are substituted into the
            function which should be zero.
        force=True (default is False)
            Make positive all symbols without assumptions regarding sign.
        rational=True (default)
            Recast Floats as Rational; if this option is not used, the
            system containing Floats may fail to solve because of issues
            with polys. If rational=None, Floats will be recast as
            rationals but the answer will be recast as Floats. If the
            flag is False then nothing will be done to the Floats.
        manual=True (default is False)
            Do not use the polys/matrix method to solve a system of
            equations, solve them one at a time as you might "manually."
        implicit=True (default is False)
            Allows ``solve`` to return a solution for a pattern in terms of
            other functions that contain that pattern; this is only
            needed if the pattern is inside of some invertible function
            like cos, exp, etc.
        particular=True (default is False)
            Instructs ``solve`` to try to find a particular solution to
            a linear system with as many zeros as possible; this is very
            expensive.
        quick=True (default is False; ``particular`` must be True)
            Selects a fast heuristic to find a solution with many zeros
            whereas a value of False uses the very slow method guaranteed
            to find the largest number of zeros possible.
        cubics=True (default)
            Return explicit solutions when cubic expressions are encountered.
            When False, quartics and quintics are disabled, too.
        quartics=True (default)
            Return explicit solutions when quartic expressions are encountered.
            When False, quintics are disabled, too.
        quintics=True (default)
            Return explicit solutions (if possible) when quintic expressions
            are encountered.

    See Also
    ========

    rsolve: For solving recurrence relationships
    sympy.solvers.ode.dsolve: For solving differential equations

    """
    from .inequalities import reduce_inequalities

    # checking/recording flags
    ###########################################################################

    # set solver types explicitly; as soon as one is False
    # all the rest will be False
    hints = ('cubics', 'quartics', 'quintics')
    default = True
    for k in hints:
        default = flags.setdefault(k, bool(flags.get(k, default)))

    # allow solution to contain symbol if True:
    implicit = flags.get('implicit', False)

    # record desire to see warnings
    warn = flags.get('warn', False)

    # this flag will be needed for quick exits below, so record
    # now -- but don't record `dict` yet since it might change
    as_set = flags.get('set', False)

    # keeping track of how f was passed
    bare_f = not iterable(f)

    # check flag usage for particular/quick which should only be used
    # with systems of equations
    if flags.get('quick', None) is not None:
        if not flags.get('particular', None):
            raise ValueError('when using `quick`, `particular` should be True')
    if flags.get('particular', False) and bare_f:
        raise ValueError(filldedent("""
            The 'particular/quick' flag is usually used with systems of
            equations. Either pass your equation in a list or
            consider using a solver like `diophantine` if you are
            looking for a solution in integers."""))

    # sympify everything, creating list of expressions and list of symbols
    ###########################################################################

    def _sympified_list(w):
        return list(map(sympify, w if iterable(w) else [w]))
    f, symbols = (_sympified_list(w) for w in [f, symbols])

    # preprocess symbol(s)
    ###########################################################################

    ordered_symbols = None  # were the symbols in a well defined order?
    if not symbols:
        # get symbols from equations
        symbols = set().union(*[fi.free_symbols for fi in f])
        if len(symbols) < len(f):
            for fi in f:
                pot = preorder_traversal(fi)
                for p in pot:
                    if isinstance(p, AppliedUndef):
                        if not as_set:
                            flags['dict'] = True  # better show symbols
                        symbols.add(p)
                        pot.skip()  # don't go any deeper
        ordered_symbols = False
        symbols = list(ordered(symbols))  # to make it canonical
    else:
        if len(symbols) == 1 and iterable(symbols[0]):
            symbols = symbols[0]
        ordered_symbols = symbols and is_sequence(symbols,
                        include=GeneratorType)
        _symbols = list(uniq(symbols))
        if len(_symbols) != len(symbols):
            ordered_symbols = False
            symbols = list(ordered(symbols))
        else:
            symbols = _symbols

    # check for duplicates
    if len(symbols) != len(set(symbols)):
        raise ValueError('duplicate symbols given')
    # remove those not of interest
    exclude = flags.pop('exclude', set())
    if exclude:
        if isinstance(exclude, Expr):
            exclude = [exclude]
        exclude = set().union(*[e.free_symbols for e in sympify(exclude)])
        symbols = [s for s in symbols if s not in exclude]

    # preprocess equation(s)
    ###########################################################################

    # automatically ignore True values
    if isinstance(f, list):
        f = [s for s in f if s is not S.true]

    # handle canonicalization of equation types
    for i, fi in enumerate(f):
        if isinstance(fi, (Eq, Ne)):
            if 'ImmutableDenseMatrix' in [type(a).__name__ for a in fi.args]:
                fi = fi.lhs - fi.rhs
            else:
                L, R = fi.args
                if isinstance(R, BooleanAtom):
                    L, R = R, L
                if isinstance(L, BooleanAtom):
                    if isinstance(fi, Ne):
                        L = ~L
                    if R.is_Relational:
                        fi = ~R if L is S.false else R
                    elif R.is_Symbol:
                        return L
                    elif R.is_Boolean and (~R).is_Symbol:
                        return ~L
                    else:
                        raise NotImplementedError(filldedent('''
                            Unanticipated argument of Eq when other arg
                            is True or False.
                        '''))
                elif isinstance(fi, Eq):
                    fi = Add(fi.lhs, -fi.rhs, evaluate=False)
            f[i] = fi

        # *** dispatch and handle as a system of relationals
        # **************************************************
        if fi.is_Relational:
            if len(symbols) != 1:
                raise ValueError("can only solve for one symbol at a time")
            if warn and symbols[0].assumptions0:
                warnings.warn(filldedent("""
                    \tWarning: assumptions about variable '%s' are
                    not handled currently.""" % symbols[0]))
            return reduce_inequalities(f, symbols=symbols)

        # convert Poly to expression
        if isinstance(fi, Poly):
            f[i] = fi.as_expr()

        # rewrite hyperbolics in terms of exp if they have symbols of
        # interest
        f[i] = f[i].replace(lambda w: isinstance(w, HyperbolicFunction) and \
            w.has_free(*symbols), lambda w: w.rewrite(exp))

        # if we have a Matrix, we need to iterate over its elements again
        if f[i].is_Matrix:
            try:
                f[i] = f[i].as_explicit()
            except ValueError:
                raise ValueError(
                    "solve cannot handle matrices with symbolic shape."
                )
            bare_f = False
            f.extend(list(f[i]))
            f[i] = S.Zero

        # if we can split it into real and imaginary parts then do so
        freei = f[i].free_symbols
        if freei and all(s.is_extended_real or s.is_imaginary for s in freei):
            fr, fi = f[i].as_real_imag()
            # accept as long as new re, im, arg or atan2 are not introduced
            had = f[i].atoms(re, im, arg, atan2)
            if fr and fi and fr != fi and not any(
                    i.atoms(re, im, arg, atan2) - had for i in (fr, fi)):
                if bare_f:
                    bare_f = False
                f[i: i + 1] = [fr, fi]

    # real/imag handling -----------------------------
    if any(isinstance(fi, (bool, BooleanAtom)) for fi in f):
        if as_set:
            return [], set()
        return []

    for i, fi in enumerate(f):
        # Abs
        while True:
            was = fi
            fi = fi.replace(Abs, lambda arg:
                separatevars(Abs(arg)).rewrite(Piecewise) if arg.has(*symbols)
                else Abs(arg))
            if was == fi:
                break

        for e in fi.find(Abs):
            if e.has(*symbols):
                raise NotImplementedError('solving %s when the argument '
                    'is not real or imaginary.' % e)

        # arg
        fi = fi.replace(arg, lambda a: arg(a).rewrite(atan2).rewrite(atan))

        # save changes
        f[i] = fi

    # see if re(s) or im(s) appear
    freim = [fi for fi in f if fi.has(re, im)]
    if freim:
        irf = []
        for s in symbols:
            if s.is_real or s.is_imaginary:
                continue  # neither re(x) nor im(x) will appear
            # if re(s) or im(s) appear, the auxiliary equation must be present
            if any(fi.has(re(s), im(s)) for fi in freim):
                irf.append((s, re(s) + S.ImaginaryUnit*im(s)))
        if irf:
            for s, rhs in irf:
                f = [fi.xreplace({s: rhs}) for fi in f] + [s - rhs]
                symbols.extend([re(s), im(s)])
            if bare_f:
                bare_f = False
            flags['dict'] = True
    # end of real/imag handling  -----------------------------

    # we can solve for non-symbol entities by replacing them with Dummy symbols
    f, symbols, swap_sym = recast_to_symbols(f, symbols)
    # this set of symbols (perhaps recast) is needed below
    symset = set(symbols)

    # get rid of equations that have no symbols of interest; we don't
    # try to solve them because the user didn't ask and they might be
    # hard to solve; this means that solutions may be given in terms
    # of the eliminated equations e.g. solve((x-y, y-3), x) -> {x: y}
    newf = []
    for fi in f:
        # let the solver handle equations that..
        # - have no symbols but are expressions
        # - have symbols of interest
        # - have no symbols of interest but are constant
        # but when an expression is not constant and has no symbols of
        # interest, it can't change what we obtain for a solution from
        # the remaining equations so we don't include it; and if it's
        # zero it can be removed and if it's not zero, there is no
        # solution for the equation set as a whole
        #
        # The reason for doing this filtering is to allow an answer
        # to be obtained to queries like solve((x - y, y), x); without
        # this mod the return value is []
        ok = False
        if fi.free_symbols & symset:
            ok = True
        else:
            if fi.is_number:
                if fi.is_Number:
                    if fi.is_zero:
                        continue
                    return []
                ok = True
            else:
                if fi.is_constant():
                    ok = True
        if ok:
            newf.append(fi)
    if not newf:
        if as_set:
            return symbols, set()
        return []
    f = newf
    del newf

    # mask off any Object that we aren't going to invert: Derivative,
    # Integral, etc... so that solving for anything that they contain will
    # give an implicit solution
    seen = set()
    non_inverts = set()
    for fi in f:
        pot = preorder_traversal(fi)
        for p in pot:
            if not isinstance(p, Expr) or isinstance(p, Piecewise):
                pass
            elif (isinstance(p, bool) or
                    not p.args or
                    p in symset or
                    p.is_Add or p.is_Mul or
                    p.is_Pow and not implicit or
                    p.is_Function and not implicit) and p.func not in (re, im):
                continue
            elif p not in seen:
                seen.add(p)
                if p.free_symbols & symset:
                    non_inverts.add(p)
                else:
                    continue
            pot.skip()
    del seen
    non_inverts = dict(list(zip(non_inverts, [Dummy() for _ in non_inverts])))
    f = [fi.subs(non_inverts) for fi in f]

    # Both xreplace and subs are needed below: xreplace to force substitution
    # inside Derivative, subs to handle non-straightforward substitutions
    non_inverts = [(v, k.xreplace(swap_sym).subs(swap_sym)) for k, v in non_inverts.items()]

    # rationalize Floats
    floats = False
    if flags.get('rational', True) is not False:
        for i, fi in enumerate(f):
            if fi.has(Float):
                floats = True
                f[i] = nsimplify(fi, rational=True)

    # capture any denominators before rewriting since
    # they may disappear after the rewrite, e.g. issue 14779
    flags['_denominators'] = _simple_dens(f[0], symbols)

    # Any embedded piecewise functions need to be brought out to the
    # top level so that the appropriate strategy gets selected.
    # However, this is necessary only if one of the piecewise
    # functions depends on one of the symbols we are solving for.
    def _has_piecewise(e):
        if e.is_Piecewise:
            return e.has(*symbols)
        return any(_has_piecewise(a) for a in e.args)
    for i, fi in enumerate(f):
        if _has_piecewise(fi):
            f[i] = piecewise_fold(fi)

    # expand angles of sums; in general, expand_trig will allow
    # more roots to be found but this is not a great solultion
    # to not returning a parametric solution, otherwise
    # many values can be returned that have a simple
    # relationship between values
    targs = {t for fi in f for t in fi.atoms(TrigonometricFunction)}
    if len(targs) > 1:
        add, other = sift(targs, lambda x: x.args[0].is_Add, binary=True)
        add, other = [[i for i in l if i.has_free(*symbols)] for l in (add, other)]
        trep = {}
        for t in add:
            a = t.args[0]
            ind, dep = a.as_independent(*symbols)
            if dep in symbols or -dep in symbols:
                # don't let expansion expand wrt anything in ind
                n = Dummy() if not ind.is_Number else ind
                trep[t] = TR10(t.func(dep + n)).xreplace({n: ind})
        if other and len(other) <= 2:
            base = gcd(*[i.args[0] for i in other]) if len(other) > 1 else other[0].args[0]
            for i in other:
                trep[i] = TR11(i, base)
        f = [fi.xreplace(trep) for fi in f]

    #
    # try to get a solution
    ###########################################################################
    if bare_f:
        solution = None
        if len(symbols) != 1:
            solution = _solve_undetermined(f[0], symbols, flags)
        if not solution:
            solution = _solve(f[0], *symbols, **flags)
    else:
        linear, solution = _solve_system(f, symbols, **flags)
    assert type(solution) is list
    assert not solution or type(solution[0]) is dict, solution
    #
    # postprocessing
    ###########################################################################
    # capture as_dict flag now (as_set already captured)
    as_dict = flags.get('dict', False)

    # define how solution will get unpacked
    tuple_format = lambda s: [tuple([i.get(x, x) for x in symbols]) for i in s]
    if as_dict or as_set:
        unpack = None
    elif bare_f:
        if len(symbols) == 1:
            unpack = lambda s: [i[symbols[0]] for i in s]
        elif len(solution) == 1 and len(solution[0]) == len(symbols):
            # undetermined linear coeffs solution
            unpack = lambda s: s[0]
        elif ordered_symbols:
            unpack = tuple_format
        else:
            unpack = lambda s: s
    else:
        if solution:
            if linear and len(solution) == 1:
                # if you want the tuple solution for the linear
                # case, use `set=True`
                unpack = lambda s: s[0]
            elif ordered_symbols:
                unpack = tuple_format
            else:
                unpack = lambda s: s
        else:
            unpack = None

    # Restore masked-off objects
    if non_inverts and type(solution) is list:
        solution = [{k: v.subs(non_inverts) for k, v in s.items()}
            for s in solution]

    # Restore original "symbols" if a dictionary is returned.
    # This is not necessary for
    #   - the single univariate equation case
    #     since the symbol will have been removed from the solution;
    #   - the nonlinear poly_system since that only supports zero-dimensional
    #     systems and those results come back as a list
    #
    # ** unless there were Derivatives with the symbols, but those were handled
    #    above.
    if swap_sym:
        symbols = [swap_sym.get(k, k) for k in symbols]
        for i, sol in enumerate(solution):
            solution[i] = {swap_sym.get(k, k): v.subs(swap_sym)
                      for k, v in sol.items()}

    # Get assumptions about symbols, to filter solutions.
    # Note that if assumptions about a solution can't be verified, it is still
    # returned.
    check = flags.get('check', True)

    # restore floats
    if floats and solution and flags.get('rational', None) is None:
        solution = nfloat(solution, exponent=False)
        # nfloat might reveal more duplicates
        solution = _remove_duplicate_solutions(solution)

    if check and solution:  # assumption checking
        warn = flags.get('warn', False)
        got_None = []  # solutions for which one or more symbols gave None
        no_False = []  # solutions for which no symbols gave False
        for sol in solution:
            v = fuzzy_and(check_assumptions(val, **symb.assumptions0)
                          for symb, val in sol.items())
            if v is False:
                continue
            no_False.append(sol)
            if v is None:
                got_None.append(sol)

        solution = no_False
        if warn and got_None:
            warnings.warn(filldedent("""
                \tWarning: assumptions concerning following solution(s)
                cannot be checked:""" + '\n\t' +
                ', '.join(str(s) for s in got_None)))

    #
    # done
    ###########################################################################

    if not solution:
        if as_set:
            return symbols, set()
        return []

    # make orderings canonical for list of dictionaries
    if not as_set:  # for set, no point in ordering
        solution = [{k: s[k] for k in ordered(s)} for s in solution]
        solution.sort(key=default_sort_key)

    if not (as_set or as_dict):
        return unpack(solution)

    if as_dict:
        return solution

    # set output: (symbols, {t1, t2, ...}) from list of dictionaries;
    # include all symbols for those that like a verbose solution
    # and to resolve any differences in dictionary keys.
    #
    # The set results can easily be used to make a verbose dict as
    #   k, v = solve(eqs, syms, set=True)
    #   sol = [dict(zip(k,i)) for i in v]
    #
    if ordered_symbols:
        k = symbols  # keep preferred order
    else:
        # just unify the symbols for which solutions were found
        k = list(ordered(set(flatten(tuple(i.keys()) for i in solution))))
    return k, {tuple([s.get(ki, ki) for ki in k]) for s in solution}


def solve(a, b, lower=False, overwrite_a=False,
          overwrite_b=False, check_finite=True, assume_a=None,
          transposed=False):
    """
    Solve the equation ``a @ x = b`` for  ``x``,
    where `a` is a square matrix.

    If the data matrix is known to be a particular type then supplying the
    corresponding string to ``assume_a`` key chooses the dedicated solver.
    The available options are

    =============================  ================================
     diagonal                       'diagonal'
     tridiagonal                    'tridiagonal'
     banded                         'banded'
     upper triangular               'upper triangular'
     lower triangular               'lower triangular'
     symmetric                      'symmetric' (or 'sym')
     hermitian                      'hermitian' (or 'her')
     symmetric positive definite    'positive definite' (or 'pos')
     general                        'general' (or 'gen')
    =============================  ================================

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : array_like, shape (..., N, N)
        Square left-hand side matrix or a batch of matrices.
    b : (..., N, NRHS) array_like
        Input data for the right hand side or a batch of right-hand sides.
    lower : bool, default: False
        Ignored unless ``assume_a`` is one of ``'sym'``, ``'her'``, or ``'pos'``.
        If True, the calculation uses only the data in the lower triangle of `a`;
        entries above the diagonal are ignored. If False (default), the
        calculation uses only the data in the upper triangle of `a`; entries
        below the diagonal are ignored.
    overwrite_a : bool, optional
        Allow overwriting data in `a` (may enhance performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_b : bool, optional
        Allow overwriting data in `b` (may enhance performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, default: True
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    assume_a : str, optional
        Valid entries are described above.
        If omitted or ``None``, checks are performed to identify structure so the
        appropriate solver can be called.
    transposed : bool, default: False
        If True, solve ``a.T @ x == b``. Raises `NotImplementedError`
        for complex `a`.

    Returns
    -------
    x : ndarray, shape (N, NRHS) or (..., N)
        The solution array.

    Raises
    ------
    ValueError
        If size mismatches detected or input a is not square.
    LinAlgError
        If the computation fails because of matrix singularity.
    LinAlgWarning
        If an ill-conditioned input a is detected.
    NotImplementedError
        If transposed is True and input a is a complex matrix.

    Notes
    -----
    If the input b matrix is a 1-D array with N elements, when supplied
    together with an NxN input a, it is assumed as a valid column vector
    despite the apparent size mismatch. This is compatible with the
    numpy.dot() behavior and the returned result is still 1-D array.

    The general, symmetric, Hermitian and positive definite solutions are
    obtained via calling ?GETRF/?GETRS, ?SYSV, ?HESV, and ?POTRF/?POTRS routines of
    LAPACK respectively.

    The datatype of the arrays define which solver is called regardless
    of the values. In other words, even when the complex array entries have
    precisely zero imaginary parts, the complex solver will be called based
    on the data type of the array.

    Examples
    --------
    Given `a` and `b`, solve for `x`:

    >>> import numpy as np
    >>> a = np.array([[3, 2, 0], [1, -1, 0], [0, 5, 1]])
    >>> b = np.array([2, 4, -1])
    >>> from scipy.linalg import solve
    >>> x = solve(a, b)
    >>> x
    array([ 2., -2.,  9.])
    >>> a @ x == b
    array([ True,  True,  True], dtype=bool)

    Batches of matrices are supported, with and without structure detection:
    (See :ref:`linalg_batch` for further details of handling batched inputs.)

    >>> a = np.arange(12).reshape(3, 2, 2)   # a batch of 3 2x2 matrices
    >>> A = a.transpose(0, 2, 1) @ a    # A is a batch of 3 positive definite matrices
    >>> b = np.ones(2)
    >>> solve(A, b)      # this automatically detects that A is pos.def.
    array([[ 1. , -0.5],
           [ 3. , -2.5],
           [ 5. , -4.5]])
    >>> solve(A, b, assume_a='pos')   # bypass structucture detection
    array([[ 1. , -0.5],
           [ 3. , -2.5],
           [ 5. , -4.5]])

    Note that the structure detection runs per-slice: in the example above, each of the
    two slices will be independently discovered as being positive definite. Setting an
    explicit ``assume_a`` argument bypasses structure detection and uses the provided
    value without checking:

    >>> a = np.stack((np.eye(2), np.arange(1, 5).reshape(2, 2)))
    >>> b = [1, 1]
    >>> solve(a, b, assume_a="diagonal")
    array([[1.  , 1.  ],
           [1.  , 0.25]])   # the second row is incorrect
    """
    # keep the numbers in sync with C
    structure = {
        None: -1,
        'general': 0, 'gen': 0,
        'diagonal': 11,
        'tridiagonal': 31,
        'banded': 41,
        'upper triangular': 21,
        'lower triangular': 22,
        'pos' : 101, 'positive definite': 101,
        'sym' : 201, 'symmetric': 201,
        'her' : 211, 'hermitian': 211,
    }.get(assume_a, 'unknown')
    if structure == 'unknown':
        raise ValueError(f'{assume_a} is not a recognized matrix structure')

    a1 = np.atleast_2d(_asarray_validated(a, check_finite=check_finite))
    b1 = np.atleast_1d(_asarray_validated(b, check_finite=check_finite))
    _deprecate_dtypes("linalg.solve", a1, b1)

    a1, b1 = _ensure_dtype_cdsz(a1, b1)   # XXX; b upcasts a?
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)
    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)
    b1, overwrite_b = _ensure_aligned_and_native(b1, overwrite_b)

    if a1.ndim < 2:
        raise ValueError(f"Expected at least ndim=2, got {a1.ndim=}")
    if a1.shape[-1] != a1.shape[-2]:
        raise ValueError(f"Expected square matrix, got {a1.shape=}")

    # backwards compatibility
    if np.issubdtype(a1.dtype, np.complexfloating) and transposed:
        raise NotImplementedError('scipy.linalg.solve can currently '
                                  'not solve a^T x = b or a^H x = b '
                                  'for complex matrices.')

    # align the shape of b with a: 1. make b1 at least 2D
    b_is_1D = b1.ndim == 1
    if b_is_1D:
        b1 = b1[:, None]

    a_is_scalar = a1.size == 1

    if b1.shape[-2] != a1.shape[-1] and not a_is_scalar:
        raise ValueError(f"incompatible shapes: {a1.shape=} and {b1.shape=}")

    # 2. broadcast the batch dimensions of b1 and a1
    batch_shape = np.broadcast_shapes(a1.shape[:-2], b1.shape[:-2])
    a1 = np.broadcast_to(a1, batch_shape + a1.shape[-2:])
    b1 = np.broadcast_to(b1, batch_shape + b1.shape[-2:])

    # catch empty inputs
    if a1.size == 0 or b1.size == 0:
        x = np.empty_like(b1)
        if b_is_1D:
            x = x[..., 0]
        return x

    if a_is_scalar:
        if a1.item() == 0:
            raise LinAlgError("A singular matrix detected.")

        out = b1 / a1
        return out[..., 0] if b_is_1D else out

    # XXX a1.ndim > 2 ; b1.ndim > 2
    # XXX can do something if a1 C ordered & transposed==True ?
    overwrite_a = overwrite_a and (a1.ndim == 2) and (a1.flags["F_CONTIGUOUS"])
    overwrite_b = overwrite_b and (b1.ndim <= 2) and (b1.flags["F_CONTIGUOUS"])

    # heavy lifting
    x, err_lst = _batched_linalg._solve(
        a1, b1, structure, lower, transposed, overwrite_a, overwrite_b
    )

    if err_lst:
        _format_emit_errors_warnings(err_lst)

    if b_is_1D:
        x = x[..., 0]
    return x


def solve(x1: Array, x2: Array, /) -> Array:
    try:
        from numpy.linalg._linalg import (  # type: ignore[attr-defined]
            _assert_stacked_2d,
            _assert_stacked_square,
            _commonType,
            _makearray,
            _raise_linalgerror_singular,
            isComplexType,
        )
    except ImportError:
        from numpy.linalg.linalg import (  # type: ignore[attr-defined]
            _assert_stacked_2d,
            _assert_stacked_square,
            _commonType,
            _makearray,
            _raise_linalgerror_singular,
            isComplexType,
        )
    from numpy.linalg import _umath_linalg

    x1, _ = _makearray(x1)
    _assert_stacked_2d(x1)
    _assert_stacked_square(x1)
    x2, wrap = _makearray(x2)
    t, result_t = _commonType(x1, x2)

    # This part is different from np.linalg.solve
    gufunc: np.ufunc
    if x2.ndim == 1:
        gufunc = _umath_linalg.solve1
    else:
        gufunc = _umath_linalg.solve

    # This does nothing currently but is left in because it will be relevant
    # when complex dtype support is added to the spec in 2022.
    signature = "DD->D" if isComplexType(t) else "dd->d"
    with np.errstate(
        call=_raise_linalgerror_singular,
        invalid="call",
        over="ignore",
        divide="ignore",
        under="ignore",
    ):
        r: Array = gufunc(x1, x2, signature=signature)

    return wrap(r.astype(result_t, copy=False))


def solve(x1: Array, x2: Array, /, **kwargs: object) -> Array:
    x1, x2 = _fix_promotion(x1, x2, only_scalar=False)
    # Torch tries to emulate NumPy 1 solve behavior by using batched 1-D solve
    # whenever
    # 1. x1.ndim - 1 == x2.ndim
    # 2. x1.shape[:-1] == x2.shape
    #
    # See linalg_solve_is_vector_rhs in
    # aten/src/ATen/native/LinearAlgebraUtils.h and
    # TORCH_META_FUNC(_linalg_solve_ex) in
    # aten/src/ATen/native/BatchLinearAlgebra.cpp in the PyTorch source code.
    #
    # The easiest way to work around this is to prepend a size 1 dimension to
    # x2, since x2 is already one dimension less than x1.
    #
    # See https://github.com/pytorch/pytorch/issues/52915
    if x2.ndim != 1 and x1.ndim - 1 == x2.ndim and x1.shape[:-1] == x2.shape:
        x2 = x2[None]
    return torch.linalg.solve(x1, x2, **kwargs)


def solve(a, b):
    """
    Solve a linear matrix equation, or system of linear scalar equations.

    Computes the "exact" solution, `x`, of the well-determined, i.e., full
    rank, linear matrix equation `ax = b`.

    Parameters
    ----------
    a : (..., M, M) array_like
        Coefficient matrix.
    b : {(M,), (..., M, K)}, array_like
        Ordinate or "dependent variable" values.

    Returns
    -------
    x : {(..., M,), (..., M, K)} ndarray
        Solution to the system a x = b.  Returned shape is (..., M) if b is
        shape (M,) and (..., M, K) if b is (..., M, K), where the "..." part is
        broadcasted between a and b.

    Raises
    ------
    LinAlgError
        If `a` is singular or not square.

    See Also
    --------
    scipy.linalg.solve : Similar function in SciPy.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The solutions are computed using LAPACK routine ``_gesv``.

    `a` must be square and of full-rank, i.e., all rows (or, equivalently,
    columns) must be linearly independent; if either is not true, use
    `lstsq` for the least-squares best "solution" of the
    system/equation.

    .. versionchanged:: 2.0

       The b array is only treated as a shape (M,) column vector if it is
       exactly 1-dimensional. In all other instances it is treated as a stack
       of (M, K) matrices. Previously b would be treated as a stack of (M,)
       vectors if b.ndim was equal to a.ndim - 1.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pg. 22.

    Examples
    --------
    Solve the system of equations:
    ``x0 + 2 * x1 = 1`` and
    ``3 * x0 + 5 * x1 = 2``:

    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 5]])
    >>> b = np.array([1, 2])
    >>> x = np.linalg.solve(a, b)
    >>> x
    array([-1.,  1.])

    Check that the solution is correct:

    >>> np.allclose(np.dot(a, x), b)
    True

    """
    a, _ = _makearray(a)
    _assert_stacked_square(a)
    b, wrap = _makearray(b)
    t, result_t = _commonType(a, b)

    # We use the b = (..., M,) logic, only if the number of extra dimensions
    # match exactly
    if b.ndim == 1:
        gufunc = _umath_linalg.solve1
    else:
        gufunc = _umath_linalg.solve

    signature = 'DD->D' if isComplexType(t) else 'dd->d'
    with errstate(call=_raise_linalgerror_singular, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        r = gufunc(a, b, signature=signature)

    return wrap(r.astype(result_t, copy=False))


def solve(a: ArrayLike, b: ArrayLike) -> Array:
  """Solve a linear system of equations.

  JAX implementation of :func:`numpy.linalg.solve`.

  This solves a (batched) linear system of equations ``a @ x = b``
  for ``x`` given ``a`` and ``b``.

  If ``a`` is singular, this will return ``nan`` or ``inf`` values.

  Args:
    a: array of shape ``(..., N, N)``.
    b: array of shape ``(N,)`` (for 1-dimensional right-hand-side) or
      ``(..., N, M)`` (for batched 2-dimensional right-hand-side).

  Returns:
    An array containing the result of the linear solve if ``a`` is non-singular.
    The result has shape ``(..., N)`` if ``b`` is of shape ``(N,)``, and has
    shape ``(..., N, M)`` otherwise.
    If ``a`` is singular, the result contains ``nan`` or ``inf`` values.

  See also:
    - :func:`jax.scipy.linalg.solve`: SciPy-style API for solving linear systems.
    - :func:`jax.lax.custom_linear_solve`: matrix-free linear solver.

  Examples:
    A simple 3x3 linear system:

    >>> A = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> b = jnp.array([14., 16., 10.])
    >>> x = jnp.linalg.solve(A, b)
    >>> x
    Array([1., 2., 3.], dtype=float32)

    Confirming that the result solves the system:

    >>> jnp.allclose(A @ x, b)
    Array(True, dtype=bool)
  """
  a, b = ensure_arraylike("jnp.linalg.solve", a, b)
  a, b = promote_dtypes_inexact(a, b)

  if a.ndim < 2:
    raise ValueError(
      f"left hand array must be at least two dimensional; got {a.shape=}")

  # Check for invalid inputs that previously would have led to a batched 1D solve:
  if (b.ndim > 1 and a.ndim == b.ndim + 1 and
      a.shape[-1] == b.shape[-1] and a.shape[-1] != b.shape[-2]):
    raise ValueError(
      f"Invalid shapes for solve: {a.shape}, {b.shape}. Prior to JAX v0.5.0,"
      " this would have been treated as a batched 1-dimensional solve."
      " To recover this behavior, use solve(a, b[..., None]).squeeze(-1).")

  signature = "(m,m),(m)->(m)" if b.ndim == 1 else "(m,m),(m,n)->(m,n)"
  a, b = core.auto_insert_reshard(a, b)
  return jnp.vectorize(lax_linalg._solve, signature=signature)(a, b)


def solve(a: ArrayLike, b: ArrayLike, lower: bool = False,
          overwrite_a: bool = False, overwrite_b: bool = False, debug: bool = False,
          check_finite: bool = True, assume_a: str = 'gen') -> Array:
  """Solve a linear system of equations.

  JAX implementation of :func:`scipy.linalg.solve`.

  This solves a (batched) linear system of equations ``a @ x = b`` for ``x``
  given ``a`` and ``b``.

  If ``a`` is singular, this will return ``nan`` or ``inf`` values.

  Args:
    a: array of shape ``(..., N, N)``.
    b: array of shape ``(..., N)`` or ``(..., N, M)``
    lower: Referenced only if ``assume_a != 'gen'``. If True, only use the lower
      triangle of the input, If False (default), only use the upper triangle.
    assume_a: specify what properties of ``a`` can be assumed. Options are:

      - ``"gen"``: generic matrix (default)
      - ``"sym"``: symmetric matrix
      - ``"her"``: hermitian matrix
      - ``"pos"``: positive-definite matrix

    overwrite_a: unused by JAX
    overwrite_b: unused by JAX
    debug: unused by JAX
    check_finite: unused by JAX

  Returns:
    An array of the same shape as ``b`` containing the solution to the linear
    system if ``a`` is non-singular.
    If ``a`` is singular, the result contains ``nan`` or ``inf`` values.

  See also:
    - :func:`jax.scipy.linalg.lu_solve`: Solve via LU factorization.
    - :func:`jax.scipy.linalg.cho_solve`: Solve via Cholesky factorization.
    - :func:`jax.scipy.linalg.solve_triangular`: Solve a triangular system.
    - :func:`jax.numpy.linalg.solve`: NumPy-style API for solving linear systems.
    - :func:`jax.lax.custom_linear_solve`: matrix-free linear solver.

  Examples:
    A simple 3x3 linear system:

    >>> A = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> b = jnp.array([14., 16., 10.])
    >>> x = jax.scipy.linalg.solve(A, b)
    >>> x
    Array([1., 2., 3.], dtype=float32)

    Confirming that the result solves the system:

    >>> jnp.allclose(A @ x, b)
    Array(True, dtype=bool)
  """
  del overwrite_a, overwrite_b, debug, check_finite  #unused
  valid_assume_a = ['gen', 'sym', 'her', 'pos']
  if assume_a not in valid_assume_a:
    raise ValueError(f"Expected assume_a to be one of {valid_assume_a}; got {assume_a!r}")
  return _solve(a, b, assume_a, lower)

