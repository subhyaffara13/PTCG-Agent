
def can_do_meijer(a1, a2, b1, b2, numeric=True):
    """
    This helper function tries to hyperexpand() the meijer g-function
    corresponding to the parameters a1, a2, b1, b2.
    It returns False if this expansion still contains g-functions.
    If numeric is True, it also tests the so-obtained formula numerically
    (at random values) and returns False if the test fails.
    Else it returns True.
    """
    from sympy.core.function import expand
    from sympy.functions.elementary.complexes import unpolarify
    r = hyperexpand(meijerg(a1, a2, b1, b2, z))
    if r.has(meijerg):
        return False
    # NOTE hyperexpand() returns a truly branched function, whereas numerical
    #      evaluation only works on the main branch. Since we are evaluating on
    #      the main branch, this should not be a problem, but expressions like
    #      exp_polar(I*pi/2*x)**a are evaluated incorrectly. We thus have to get
    #      rid of them. The expand heuristically does this...
    r = unpolarify(expand(r, force=True, power_base=True, power_exp=False,
                          mul=False, log=False, multinomial=False, basic=False))

    if not numeric:
        return True

    repl = {}
    for n, ai in enumerate(meijerg(a1, a2, b1, b2, z).free_symbols - {z}):
        repl[ai] = randcplx(n)
    return tn(meijerg(a1, a2, b1, b2, z).subs(repl), r.subs(repl), z)

