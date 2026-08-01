
def test_issue_2934():
    assert latex(Symbol(r'\frac{a_1}{b_1}')) == r'\frac{a_1}{b_1}'

