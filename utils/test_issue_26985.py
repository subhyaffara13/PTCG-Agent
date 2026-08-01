
def test_issue_26985():
    a, b, c, d = symbols('a b c d')

    # Expression before applying to_anf
    x = Xor(c, And(a, b), And(a, c))
    y = Xor(a, b, And(a, c))

    # Applying to_anf
    result = Xor(Xor(d, And(x, y)), And(x, y))
    result_anf = to_anf(Xor(to_anf(Xor(d, And(x, y))), And(x, y)))

    assert result_anf == d
    assert result == d

