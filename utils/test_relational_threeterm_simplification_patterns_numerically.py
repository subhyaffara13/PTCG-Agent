
def test_relational_threeterm_simplification_patterns_numerically():
    from sympy.core import Wild
    from sympy.logic.boolalg import _simplify_patterns_and3
    a = Wild('a')
    b = Wild('b')
    c = Wild('c')
    symb = [a, b, c]
    patternlists = [[And, _simplify_patterns_and3()]]
    valuelist = list(set(combinations(list(range(-2, 3)) * 3, 3)))
    # Skip combinations of +/-2 and 0, except for all 0
    valuelist = [v for v in valuelist if any(w % 2 for w in v) or not any(v)]
    for func, patternlist in patternlists:
        for pattern in patternlist:
            original = func(*pattern[0].args)
            simplified = pattern[1]
            for values in valuelist:
                sublist = dict(zip(symb, values))
                originalvalue = original.xreplace(sublist)
                simplifiedvalue = simplified.xreplace(sublist)
                assert originalvalue == simplifiedvalue, "Original: {}\nand" \
                                                         " simplified: {}\ndo not evaluate to the same value for" \
                                                         "{}".format(pattern[0], simplified, sublist)

