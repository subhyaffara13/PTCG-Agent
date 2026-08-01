
def test_pretty_primeomega():
    from sympy.functions.combinatorial.numbers import primeomega

    ascii_str1 = "Omega(n)"
    ucode_str1 = "Ω(n)"

    n = symbols('n', integer=True)
    assert pretty(primeomega(n)) == ascii_str1
    assert upretty(primeomega(n)) == ucode_str1

