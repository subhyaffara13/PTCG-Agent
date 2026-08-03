import re

def _get_const_characteristic_eq_sols(r, func, order):
    r"""
    Returns the roots of characteristic equation of constant coefficient
    linear ODE and list of collectterms which is later on used by simplification
    to use collect on solution.

    The parameter `r` is a dict of order:coeff terms, where order is the order of the
    derivative on each term, and coeff is the coefficient of that derivative.

    """
    x = func.args[0]
    # First, set up characteristic equation.
    chareq, symbol = S.Zero, Dummy('x')

    for i in r.keys():
        if isinstance(i, str) or i < 0:
            pass
        else:
            chareq += r[i]*symbol**i

    chareq = Poly(chareq, symbol)
    # Can't just call roots because it doesn't return rootof for unsolveable
    # polynomials.
    chareqroots = roots(chareq, multiple=True)
    if len(chareqroots) != order:
        chareqroots = [rootof(chareq, k) for k in range(chareq.degree())]

    chareq_is_complex = not all(i.is_real for i in chareq.all_coeffs())

    # Create a dict root: multiplicity or charroots
    charroots = Counter(chareqroots)
    # We need to keep track of terms so we can run collect() at the end.
    # This is necessary for constantsimp to work properly.
    collectterms = []
    gensols = []
    conjugate_roots = [] # used to prevent double-use of conjugate roots
    # Loop over roots in theorder provided by roots/rootof...
    for root in chareqroots:
        # but don't repoeat multiple roots.
        if root not in charroots:
            continue
        multiplicity = charroots.pop(root)
        for i in range(multiplicity):
            if chareq_is_complex:
                gensols.append(x**i*exp(root*x))
                collectterms = [(i, root, 0)] + collectterms
                continue
            reroot = re(root)
            imroot = im(root)
            if imroot.has(atan2) and reroot.has(atan2):
                # Remove this condition when re and im stop returning
                # circular atan2 usages.
                gensols.append(x**i*exp(root*x))
                collectterms = [(i, root, 0)] + collectterms
            else:
                if root in conjugate_roots:
                    collectterms = [(i, reroot, imroot)] + collectterms
                    continue
                if imroot == 0:
                    gensols.append(x**i*exp(reroot*x))
                    collectterms = [(i, reroot, 0)] + collectterms
                    continue
                conjugate_roots.append(conjugate(root))
                gensols.append(x**i*exp(reroot*x) * sin(abs(imroot) * x))
                gensols.append(x**i*exp(reroot*x) * cos(    imroot  * x))

                # This ordering is important
                collectterms = [(i, reroot, imroot)] + collectterms
    return gensols, collectterms

