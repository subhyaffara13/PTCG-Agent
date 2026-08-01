
def test_latex_SetExpr():
    iv = Interval(1, 3)
    se = SetExpr(iv)
    assert latex(se) == r"SetExpr\left(\left[1, 3\right]\right)"

