
def test_pretty_primenu():
    from sympy.functions.combinatorial.numbers import primenu

    ascii_str1 = "nu(n)"
    ucode_str1 = "ν(n)"

    n = symbols('n', integer=True)
    assert pretty(primenu(n)) == ascii_str1
    assert upretty(primenu(n)) == ucode_str1

