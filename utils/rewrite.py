
def rewrite(
    path: StrPath,
    encoding: Optional[str],
    follow_symlinks: bool = False,
) -> Iterator[Tuple[IO[str], IO[str]]]:
    if follow_symlinks:
        path = os.path.realpath(path)

    try:
        source: IO[str] = open(path, encoding=encoding)
        try:
            path_stat = os.lstat(path)
            original_mode: Optional[int] = (
                stat.S_IMODE(path_stat.st_mode)
                if stat.S_ISREG(path_stat.st_mode)
                else None
            )
        except BaseException:
            source.close()
            raise
    except FileNotFoundError:
        source = io.StringIO("")
        original_mode = None

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding=encoding,
        delete=False,
        prefix=".tmp_",
        dir=os.path.dirname(os.path.abspath(path)),
    ) as dest:
        dest_path = pathlib.Path(dest.name)
        error = None

        try:
            with source:
                yield (source, dest)
        except BaseException as err:
            error = err

    if error is None:
        try:
            if original_mode is not None:
                os.chmod(dest_path, original_mode)

            os.replace(dest_path, path)
        except BaseException:
            dest_path.unlink(missing_ok=True)
            raise
    else:
        dest_path.unlink(missing_ok=True)
        raise error from None


def rewrite(C, alpha, w):
    """
    Parameters
    ==========

    C: CosetTable
    alpha: A live coset
    w: A word in `A*`

    Returns
    =======

    rho(tau(alpha), w)

    Examples
    ========

    >>> from sympy.combinatorics.fp_groups import FpGroup, CosetTable, define_schreier_generators, rewrite
    >>> from sympy.combinatorics import free_group
    >>> F, x, y = free_group("x, y")
    >>> f = FpGroup(F, [x**2, y**3, (x*y)**6])
    >>> C = CosetTable(f, [])
    >>> C.table = [[1, 1, 2, 3], [0, 0, 4, 5], [4, 4, 3, 0], [5, 5, 0, 2], [2, 2, 5, 1], [3, 3, 1, 4]]
    >>> C.p = [0, 1, 2, 3, 4, 5]
    >>> define_schreier_generators(C)
    >>> rewrite(C, 0, (x*y)**6)
    x_4*y_2*x_3*x_1*x_2*y_4*x_5

    """
    v = C._schreier_free_group.identity
    for i in range(len(w)):
        x_i = w[i]
        v = v*C.P[alpha][C.A_dict[x_i]]
        alpha = C.table[alpha][C.A_dict[x_i]]
    return v


def rewrite(e, Omega, x, wsym):
    """e(x) ... the function
    Omega ... the mrv set
    wsym ... the symbol which is going to be used for w

    Returns the rewritten e in terms of w and log(w). See test_rewrite1()
    for examples and correct results.
    """

    from sympy import AccumBounds
    if not isinstance(Omega, SubsSet):
        raise TypeError("Omega should be an instance of SubsSet")
    if len(Omega) == 0:
        raise ValueError("Length cannot be 0")
    # all items in Omega must be exponentials
    for t in Omega.keys():
        if not isinstance(t, exp):
            raise ValueError("Value should be exp")
    rewrites = Omega.rewrites
    Omega = list(Omega.items())

    nodes = build_expression_tree(Omega, rewrites)
    Omega.sort(key=lambda x: nodes[x[1]].ht(), reverse=True)

    # make sure we know the sign of each exp() term; after the loop,
    # g is going to be the "w" - the simplest one in the mrv set
    for g, _ in Omega:
        sig = sign(g.exp, x)
        if sig != 1 and sig != -1 and not sig.has(AccumBounds):
            raise NotImplementedError('Result depends on the sign of %s' % sig)
    if sig == 1:
        wsym = 1/wsym  # if g goes to oo, substitute 1/w
    # O2 is a list, which results by rewriting each item in Omega using "w"
    O2 = []
    denominators = []
    for f, var in Omega:
        c = limitinf(f.exp/g.exp, x)
        if c.is_Rational:
            denominators.append(c.q)
        arg = f.exp
        if var in rewrites:
            if not isinstance(rewrites[var], exp):
                raise ValueError("Value should be exp")
            arg = rewrites[var].args[0]
        O2.append((var, exp((arg - c*g.exp))*wsym**c))

    # Remember that Omega contains subexpressions of "e". So now we find
    # them in "e" and substitute them for our rewriting, stored in O2

    # the following powsimp is necessary to automatically combine exponentials,
    # so that the .xreplace() below succeeds:
    # TODO this should not be necessary
    from sympy.simplify.powsimp import powsimp
    f = powsimp(e, deep=True, combine='exp')
    for a, b in O2:
        f = f.xreplace({a: b})

    for _, var in Omega:
        assert not f.has(var)

    # finally compute the logarithm of w (logw).
    logw = g.exp
    if sig == 1:
        logw = -logw  # log(w)->log(1/w)=-log(w)

    # Some parts of SymPy have difficulty computing series expansions with
    # non-integral exponents. The following heuristic improves the situation:
    exponent = reduce(ilcm, denominators, 1)
    f = f.subs({wsym: wsym**exponent})
    logw /= exponent

    # bottom_up function is required for a specific case - when f is
    # -exp(p/(p + 1)) + exp(-p**2/(p + 1) + p). No current simplification
    # methods reduce this to 0 while not expanding polynomials.
    f = bottom_up(f, lambda w: getattr(w, 'normal', lambda: w)())

    return f, logw

