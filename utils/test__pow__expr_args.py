
def test_Pow_Expr_args():
    bases = [Basic(), Poly(x, x), FiniteSet(x)]
    for base in bases:
        # The cache can mess with the stacklevel test
        with warns(SymPyDeprecationWarning, test_stacklevel=False):
            Pow(base, S.One)

