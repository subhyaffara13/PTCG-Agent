
def _get_euler_characteristic_eq_sols(eq, func, match_obj):
    r"""
    Returns the solution of homogeneous part of the linear euler ODE and
    the list of roots of characteristic equation.

    The parameter ``match_obj`` is a dict of order:coeff terms, where order is the order
    of the derivative on each term, and coeff is the coefficient of that derivative.

    """
    x = func.args[0]
    f = func.func

    # First, set up characteristic equation.
    chareq, symbol = S.Zero, Dummy('x')

    for i in match_obj:
        if i >= 0:
            chareq += (match_obj[i]*diff(x**symbol, x, i)*x**-symbol).expand()

    chareq = Poly(chareq, symbol)
    chareqroots = [rootof(chareq, k) for k in range(chareq.degree())]
    collectterms = []

    # A generator of constants
    constants = list(get_numbered_constants(eq, num=chareq.degree()*2))
    constants.reverse()

    # Create a dict root: multiplicity or charroots
    charroots = Counter(chareqroots)
    gsol = S.Zero
    ln = log
    for root, multiplicity in charroots.items():
        for i in range(multiplicity):
            if isinstance(root, RootOf):
                gsol += (x**root) * constants.pop()
                if multiplicity != 1:
                    raise ValueError("Value should be 1")
                collectterms = [(0, root, 0)] + collectterms
            elif root.is_real:
                gsol += ln(x)**i*(x**root) * constants.pop()
                collectterms = [(i, root, 0)] + collectterms
            else:
                reroot = re(root)
                imroot = im(root)
                gsol += ln(x)**i * (x**reroot) * (
                    constants.pop() * sin(abs(imroot)*ln(x))
                    + constants.pop() * cos(imroot*ln(x)))
                collectterms = [(i, reroot, imroot)] + collectterms

    gsol = Eq(f(x), gsol)

    gensols = []
    # Keep track of when to use sin or cos for nonzero imroot
    for i, reroot, imroot in collectterms:
        if imroot == 0:
            gensols.append(ln(x)**i*x**reroot)
        else:
            sin_form = ln(x)**i*x**reroot*sin(abs(imroot)*ln(x))
            if sin_form in gensols:
                cos_form = ln(x)**i*x**reroot*cos(imroot*ln(x))
                gensols.append(cos_form)
            else:
                gensols.append(sin_form)
    return gsol, gensols

