
def test_unhandled_input():
    nan = S.NaN
    bf = Q.gt(3, nan) & Q.gt(x, nan)
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(ValueError, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

    bf = Q.gt(3, I) & Q.gt(x, I)
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(UnhandledInput, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

    bf = Q.gt(3, float("inf")) & Q.gt(x, float("inf"))
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(UnhandledInput, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

    bf = Q.gt(3, oo) & Q.gt(x, oo)
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(UnhandledInput, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

    # test non-linearity
    bf = Q.gt(x**2 + x, 2)
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(UnhandledInput, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

    bf = Q.gt(cos(x) + x, 2)
    enc = boolean_formula_to_encoded_cnf(bf)
    raises(UnhandledInput, lambda: LRASolver.from_encoded_cnf(enc, testing_mode=True))

