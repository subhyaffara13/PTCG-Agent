
def test_lookup_table():
    from sympy.core.random import uniform, randrange
    from sympy.core.add import Add
    from sympy.integrals.meijerint import z as z_dummy
    table = {}
    _create_lookup_table(table)
    for l in table.values():
        for formula, terms, cond, hint in sorted(l, key=default_sort_key):
            subs = {}
            for ai in list(formula.free_symbols) + [z_dummy]:
                if hasattr(ai, 'properties') and ai.properties:
                    # these Wilds match positive integers
                    subs[ai] = randrange(1, 10)
                else:
                    subs[ai] = uniform(1.5, 2.0)
            if not isinstance(terms, list):
                terms = terms(subs)

            # First test that hyperexpand can do this.
            expanded = [hyperexpand(g) for (_, g) in terms]
            assert all(x.is_Piecewise or not x.has(meijerg) for x in expanded)

            # Now test that the meijer g-function is indeed as advertised.
            expanded = Add(*[f*x for (f, x) in terms])
            a, b = formula.n(subs=subs), expanded.n(subs=subs)
            r = min(abs(a), abs(b))
            if r < 1:
                assert abs(a - b).n() <= 1e-10
            else:
                assert (abs(a - b)/r).n() <= 1e-10

