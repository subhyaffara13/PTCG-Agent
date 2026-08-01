
def test_latex_builtins():
    assert latex(True) == r"\text{True}"
    assert latex(False) == r"\text{False}"
    assert latex(None) == r"\text{None}"
    assert latex(true) == r"\text{True}"
    assert latex(false) == r'\text{False}'

