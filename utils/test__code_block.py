
def test_CodeBlock():
    c = CodeBlock(Assignment(x, 1), Assignment(y, x + 1))
    assert c.func(*c.args) == c

    assert c.left_hand_sides == Tuple(x, y)
    assert c.right_hand_sides == Tuple(1, x + 1)

