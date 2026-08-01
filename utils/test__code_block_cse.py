
def test_CodeBlock_cse():
    c1 = CodeBlock(
        Assignment(y, 1),
        Assignment(x, sin(y)),
        Assignment(z, sin(y)),
        Assignment(t, x*z),
        )
    assert c1.cse() == CodeBlock(
        Assignment(y, 1),
        Assignment(x0, sin(y)),
        Assignment(x, x0),
        Assignment(z, x0),
        Assignment(t, x*z),
    )

    # Multiple assignments to same symbol not supported
    raises(NotImplementedError, lambda: CodeBlock(
        Assignment(x, 1),
        Assignment(y, 1), Assignment(y, 2)
    ).cse())

    # Check auto-generated symbols do not collide with existing ones
    c2 = CodeBlock(
        Assignment(x0, sin(y) + 1),
        Assignment(x1, 2 * sin(y)),
        Assignment(z, x * y),
        )
    assert c2.cse() == CodeBlock(
        Assignment(x2, sin(y)),
        Assignment(x0, x2 + 1),
        Assignment(x1, 2 * x2),
        Assignment(z, x * y),
        )

