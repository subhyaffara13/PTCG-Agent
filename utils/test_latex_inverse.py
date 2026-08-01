
def test_latex_inverse():
    # tests issue 4129
    assert latex(1/x) == r"\frac{1}{x}"
    assert latex(1/(x + y)) == r"\frac{1}{x + y}"

