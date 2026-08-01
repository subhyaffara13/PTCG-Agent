
def test_relational_simplification_numerically():
    def test_simplification_numerically_function(original, simplified):
        symb = original.free_symbols
        n = len(symb)
        valuelist = list(set(combinations(list(range(-(n - 1), n)) * n, n)))
        for values in valuelist:
            sublist = dict(zip(symb, values))
            originalvalue = original.subs(sublist)
            simplifiedvalue = simplified.subs(sublist)
            assert originalvalue == simplifiedvalue, "Original: {}\nand" \
                                                     " simplified: {}\ndo not evaluate to the same value for {}" \
                                                     "".format(original, simplified, sublist)

    w, x, y, z = symbols('w x y z', real=True)
    d, e = symbols('d e', real=False)

    expressions = (And(Eq(x, y), x >= y, w < y, y >= z, z < y),
                   And(Eq(x, y), x >= 1, 2 < y, y >= 5, z < y),
                   Or(Eq(x, y), x >= 1, 2 < y, y >= 5, z < y),
                   And(x >= y, Eq(y, x)),
                   Or(And(Eq(x, y), x >= y, w < y, Or(y >= z, z < y)),
                      And(Eq(x, y), x >= 1, 2 < y, y >= -1, z < y)),
                   (Eq(x, y) & Eq(d, e) & (x >= y) & (d >= e)),
                   )

    for expression in expressions:
        test_simplification_numerically_function(expression,
                                                 expression.simplify())

