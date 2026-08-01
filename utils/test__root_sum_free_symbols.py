
def test_RootSum_free_symbols():
    assert RootSum(x**3 + x + 3, Lambda(r, exp(r))).free_symbols == set()
    assert RootSum(x**3 + x + 3, Lambda(r, exp(a*r))).free_symbols == {a}
    assert RootSum(
        x**3 + x + y, Lambda(r, exp(a*r)), x).free_symbols == {a, y}

