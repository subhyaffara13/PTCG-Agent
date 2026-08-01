
def test_ccode_user_functions():
    x = symbols('x', integer=False)
    n = symbols('n', integer=True)
    custom_functions = {
        "ceiling": "ceil",
        "Abs": [(lambda x: not x.is_integer, "fabs"), (lambda x: x.is_integer, "abs")],
    }
    assert ccode(ceiling(x), user_functions=custom_functions) == "ceil(x)"
    assert ccode(Abs(x), user_functions=custom_functions) == "fabs(x)"
    assert ccode(Abs(n), user_functions=custom_functions) == "abs(n)"

    expr = Symbol('a')
    muladd = Function('muladd')
    for i in range(0, 100):
        # the large number of terms acts as a regression test for gh-23839
        expr = muladd(Rational(1, 2), Symbol(f'a{i}'), expr)
    out = ccode(expr, user_functions={'muladd':'muladd'})
    assert 'a99' in out
    assert out.count('muladd') == 100

