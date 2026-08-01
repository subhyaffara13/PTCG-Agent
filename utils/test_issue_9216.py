
def test_issue_9216():
    expr_1 = Pow(1, -1, evaluate=False)
    assert latex(expr_1) == r"1^{-1}"

    expr_2 = Pow(1, Pow(1, -1, evaluate=False), evaluate=False)
    assert latex(expr_2) == r"1^{1^{-1}}"

    expr_3 = Pow(3, -2, evaluate=False)
    assert latex(expr_3) == r"\frac{1}{9}"

    expr_4 = Pow(1, -2, evaluate=False)
    assert latex(expr_4) == r"1^{-2}"

