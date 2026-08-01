
def test_CodeBlock_free_symbols():
    c1 = CodeBlock(
        Assignment(x, y + z),
        Assignment(z, 1),
        Assignment(t, x),
        Assignment(y, 2),
        )
    assert c1.free_symbols == set()

    c2 = CodeBlock(
        Assignment(x, y + z),
        Assignment(z, a * b),
        Assignment(t, x),
        Assignment(y, b + 3),
    )
    assert c2.free_symbols == {a, b}

