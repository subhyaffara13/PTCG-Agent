
def test_meijerg_formulae():
    from sympy.simplify.hyperexpand import MeijerFormulaCollection
    formulae = MeijerFormulaCollection().formulae
    for sig in formulae:
        for formula in formulae[sig]:
            g = meijerg(formula.func.an, formula.func.ap,
                        formula.func.bm, formula.func.bq,
                        formula.z)
            rep = {}
            for sym in formula.symbols:
                rep[sym] = randcplx()

            # first test if the closed-form is actually correct
            g = g.subs(rep)
            closed_form = formula.closed_form.subs(rep)
            z = formula.z
            assert tn(g, closed_form, z)

            # now test the computed matrix
            cl = (formula.C * formula.B)[0].subs(rep)
            assert tn(closed_form, cl, z)
            deriv1 = z*formula.B.diff(z)
            deriv2 = formula.M * formula.B
            for d1, d2 in zip(deriv1, deriv2):
                assert tn(d1.subs(rep), d2.subs(rep), z)

