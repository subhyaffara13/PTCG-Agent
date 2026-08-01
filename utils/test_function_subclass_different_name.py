
def test_function_subclass_different_name():
    class mygamma(gamma):
        pass
    assert latex(mygamma) == r"\operatorname{mygamma}"
    assert latex(mygamma(x)) == r"\operatorname{mygamma}{\left(x \right)}"


def test_function_subclass_different_name():
    class mygamma(gamma):
        pass
    assert xpretty(mygamma, use_unicode=True) == r"mygamma"
    assert xpretty(mygamma(x), use_unicode=True) == r"mygamma(x)"

