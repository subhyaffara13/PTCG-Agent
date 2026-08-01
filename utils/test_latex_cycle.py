
def test_latex_cycle():
    assert latex(Cycle(1, 2, 4)) == r"\left( 1\; 2\; 4\right)"
    assert latex(Cycle(1, 2)(4, 5, 6)) == \
        r"\left( 1\; 2\right)\left( 4\; 5\; 6\right)"
    assert latex(Cycle()) == r"\left( \right)"

