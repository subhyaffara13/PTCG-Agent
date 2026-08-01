
def test_formulae():
    from sympy.simplify.hyperexpand import FormulaCollection
    formulae = FormulaCollection().formulae
    for formula in formulae:
        h = formula.func(formula.z)
        rep = {}
        for n, sym in enumerate(formula.symbols):
            rep[sym] = randcplx(n)

        # NOTE hyperexpand returns truly branched functions. We know we are
        #      on the main sheet, but numerical evaluation can still go wrong
        #      (e.g. if exp_polar cannot be evalf'd).
        #      Just replace all exp_polar by exp, this usually works.

        # first test if the closed-form is actually correct
        h = h.subs(rep)
        closed_form = formula.closed_form.subs(rep).rewrite('nonrepsmall')
        z = formula.z
        assert tn(h, closed_form.replace(exp_polar, exp), z)

        # now test the computed matrix
        cl = (formula.C * formula.B)[0].subs(rep).rewrite('nonrepsmall')
        assert tn(closed_form.replace(
            exp_polar, exp), cl.replace(exp_polar, exp), z)
        deriv1 = z*formula.B.applyfunc(lambda t: t.rewrite(
            'nonrepsmall')).diff(z)
        deriv2 = formula.M * formula.B
        for d1, d2 in zip(deriv1, deriv2):
            assert tn(d1.subs(rep).replace(exp_polar, exp),
                      d2.subs(rep).rewrite('nonrepsmall').replace(exp_polar, exp), z)

