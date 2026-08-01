
def test_latex_euler():
    assert latex(euler(n)) == r"E_{n}"
    assert latex(euler(n, x)) == r"E_{n}\left(x\right)"
    assert latex(euler(n, x)**2) == r"E_{n}^{2}\left(x\right)"

