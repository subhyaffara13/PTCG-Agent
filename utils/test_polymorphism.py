
def test_polymorphism():
    class A(Basic):
        def _eval_simplify(x, **kwargs):
            return S.One

    a = A(S(5), S(2))
    assert simplify(a) == 1

