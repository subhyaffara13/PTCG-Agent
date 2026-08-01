
def test_cot_series():
    assert cot(x).series(x, 0, 9) == \
        1/x - x/3 - x**3/45 - 2*x**5/945 - x**7/4725 + O(x**9)
    # issue 6210
    assert cot(x**4 + x**5).series(x, 0, 1) == \
        x**(-4) - 1/x**3 + x**(-2) - 1/x + 1 + O(x)
    assert cot(pi*(1-x)).series(x, 0, 3) == -1/(pi*x) + pi*x/3 + O(x**3)
    assert cot(x).taylor_term(0, x) == 1/x
    assert cot(x).taylor_term(2, x) is S.Zero
    assert cot(x).taylor_term(3, x) == -x**3/45

