
def test_pretty_Boolean():
    expr = Not(x, evaluate=False)

    assert pretty(expr) == "Not(x)"
    assert upretty(expr) == "¬x"

    expr = And(x, y)

    assert pretty(expr) == "And(x, y)"
    assert upretty(expr) == "x ∧ y"

    expr = Or(x, y)

    assert pretty(expr) == "Or(x, y)"
    assert upretty(expr) == "x ∨ y"

    syms = symbols('a:f')
    expr = And(*syms)

    assert pretty(expr) == "And(a, b, c, d, e, f)"
    assert upretty(expr) == "a ∧ b ∧ c ∧ d ∧ e ∧ f"

    expr = Or(*syms)

    assert pretty(expr) == "Or(a, b, c, d, e, f)"
    assert upretty(expr) == "a ∨ b ∨ c ∨ d ∨ e ∨ f"

    expr = Xor(x, y, evaluate=False)

    assert pretty(expr) == "Xor(x, y)"
    assert upretty(expr) == "x ⊻ y"

    expr = Nand(x, y, evaluate=False)

    assert pretty(expr) == "Nand(x, y)"
    assert upretty(expr) == "x ⊼ y"

    expr = Nor(x, y, evaluate=False)

    assert pretty(expr) == "Nor(x, y)"
    assert upretty(expr) == "x ⊽ y"

    expr = Implies(x, y, evaluate=False)

    assert pretty(expr) == "Implies(x, y)"
    assert upretty(expr) == "x → y"

    # don't sort args
    expr = Implies(y, x, evaluate=False)

    assert pretty(expr) == "Implies(y, x)"
    assert upretty(expr) == "y → x"

    expr = Equivalent(x, y, evaluate=False)

    assert pretty(expr) == "Equivalent(x, y)"
    assert upretty(expr) == "x ⇔ y"

    expr = Equivalent(y, x, evaluate=False)

    assert pretty(expr) == "Equivalent(x, y)"
    assert upretty(expr) == "x ⇔ y"

