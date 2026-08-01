
def test_latex_log():
    assert latex(log(x)) == r"\log{\left(x \right)}"
    assert latex(log(x), ln_notation=True) == r"\ln{\left(x \right)}"
    assert latex(log(x) + log(y)) == \
        r"\log{\left(x \right)} + \log{\left(y \right)}"
    assert latex(log(x) + log(y), ln_notation=True) == \
        r"\ln{\left(x \right)} + \ln{\left(y \right)}"
    assert latex(pow(log(x), x)) == r"\log{\left(x \right)}^{x}"
    assert latex(pow(log(x), x), ln_notation=True) == \
        r"\ln{\left(x \right)}^{x}"

