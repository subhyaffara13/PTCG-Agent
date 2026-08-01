
def test_Add_Mul_Expr_args():
    nonexpr = [Basic(), Poly(x, x), FiniteSet(x)]
    for typ in [Add, Mul]:
        for obj in nonexpr:
            # The cache can mess with the stacklevel check
            with warns(SymPyDeprecationWarning, test_stacklevel=False):
                typ(obj, 1)

